"""Train the move-prediction transformer on teacher soft targets.

Writes checkpoints/<run>/step_XXXXXX.pt on the configured schedule and runs/<run>_train.jsonl,
then results/train_curve.json (validation metrics at every eval step).
"""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from c4n import config
from c4n import engine as E
from c4n.model import C4Transformer, tokens_from_moves

CFG = config.load()
TC, MC = CFG["train"], CFG["model"]
DEV = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")


def load_split(name):
    d = np.load(config.ROOT / CFG["data"]["out_dir"] / f"{name}.npz")
    return torch.from_numpy(d["moves"]), torch.from_numpy(d["scores"]), torch.from_numpy(d["lengths"].astype(np.int64))


def targets(scores, temp):
    s = scores.float()
    legal = scores != E.ILLEGAL
    s = torch.where(legal, s / temp, torch.full_like(s, -1e9))
    return torch.softmax(s, -1), legal


def batch_metrics(model, moves, scores, lengths, temp):
    tok = tokens_from_moves(moves).to(DEV)
    logits = model(tok)[:, :42]
    p, legal = targets(scores.to(DEV), temp)
    valid = (torch.arange(42, device=DEV)[None] < lengths.to(DEV)[:, None])
    logp = F.log_softmax(logits, -1)
    ce = -(p * logp).sum(-1)
    ent = -(p * torch.log(p.clamp_min(1e-12))).sum(-1)
    kl = ce - ent
    q = logp.exp()
    legal_mass = (q * legal).sum(-1)
    sc = scores.to(DEV).float().masked_fill(~legal, -1e9)
    best = sc.max(-1, keepdim=True).values
    pick = logits.masked_fill(~legal, -1e9).argmax(-1, keepdim=True)
    agree = (sc.gather(-1, pick) == best).squeeze(-1).float()  # model's best legal move is one of the teacher's best
    raw_legal = legal.gather(-1, logits.argmax(-1, keepdim=True)).squeeze(-1).float()
    v = valid.float()
    n = v.sum()
    return dict(loss=(ce * v).sum() / n, kl=(kl * v).sum() / n, legal_mass=(legal_mass * v).sum() / n,
                agree=(agree * v).sum() / n, raw_top1_legal=(raw_legal * v).sum() / n)


@torch.no_grad()
def evaluate(model, val, temp, bs=1000):
    """Position-weighted validation metrics over the whole validation split."""
    model.eval()
    sums, total = {}, 0.0
    for i in range(0, val[0].shape[0], bs):
        npos = val[2][i:i + bs].sum().item()
        m = batch_metrics(model, val[0][i:i + bs], val[1][i:i + bs], val[2][i:i + bs], temp)
        for k, v in m.items():
            sums[k] = sums.get(k, 0.0) + v.item() * npos
        total += npos
    out = {k: v / total for k, v in sums.items()}
    model.train()
    return out


def lr_at(step):
    if step < TC["warmup"]:
        return TC["lr"] * (step + 1) / TC["warmup"]
    frac = (step - TC["warmup"]) / max(1, TC["steps"] - TC["warmup"])
    return TC["min_lr"] + 0.5 * (TC["lr"] - TC["min_lr"]) * (1 + math.cos(math.pi * frac))


def main():
    seed = TC.get("seed", CFG["seed"])  # training seed (init + data order); data generation uses CFG["seed"]
    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(seed)
    train, val = load_split("train"), load_split("val")
    train = tuple(x.to(DEV) for x in train)  # whole split lives on the accelerator (~250 MB); no CPU work per step
    model = C4Transformer(**MC).to(DEV)
    n_params = sum(p.numel() for p in model.parameters())
    decay = [p for n, p in model.named_parameters() if p.dim() >= 2]
    no_decay = [p for n, p in model.named_parameters() if p.dim() < 2]
    opt = torch.optim.AdamW([{"params": decay, "weight_decay": TC["weight_decay"]},
                             {"params": no_decay, "weight_decay": 0.0}], lr=TC["lr"], betas=(0.9, 0.95))
    out_dir = config.ROOT / TC["out_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = config.ROOT / "runs" / f"train_{Path(TC['out_dir']).name}.jsonl"
    log_path.parent.mkdir(exist_ok=True)
    log = open(log_path, "w")
    curve = []
    ckpts = set(TC["ckpt_steps"])
    N = train[0].shape[0]
    perm = torch.randperm(N, generator=gen)
    ptr = 0
    t0 = time.time()
    print(f"device {DEV}, params {n_params:,}, train games {N:,}", flush=True)
    for step in range(TC["steps"] + 1):
        if step % TC["eval_every"] == 0 or step in ckpts:
            ev = evaluate(model, val, TC["target_temp"])
            ev.update(step=step, time=round(time.time() - t0, 1))
            curve.append(ev)
            print(json.dumps({k: round(v, 4) if isinstance(v, float) else v for k, v in ev.items()}), flush=True)
        if step in ckpts:
            torch.save({"state_dict": model.state_dict(), "model_cfg": MC, "step": step, "config": CFG},
                       out_dir / f"step_{step:06d}.pt")
        if step == TC["steps"]:
            break
        if ptr + TC["batch_games"] > N:
            perm, ptr = torch.randperm(N, generator=gen), 0
        idx = perm[ptr:ptr + TC["batch_games"]].to(DEV)
        ptr += TC["batch_games"]
        for g in opt.param_groups:
            g["lr"] = lr_at(step)
        m = batch_metrics(model, train[0][idx], train[1][idx], train[2][idx], TC["target_temp"])
        opt.zero_grad(set_to_none=True)
        m["loss"].backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), TC["grad_clip"])
        opt.step()
        if step % 50 == 0:
            log.write(json.dumps({"step": step, "lr": lr_at(step), **{k: v.item() for k, v in m.items()}}) + "\n")
            log.flush()
    with open(config.results_dir(CFG) / f"train_curve_{Path(TC['out_dir']).name}.json", "w") as f:
        json.dump({"device": DEV, "params": n_params, "torch": torch.__version__, "curve": curve}, f, indent=1)


if __name__ == "__main__":
    main()
