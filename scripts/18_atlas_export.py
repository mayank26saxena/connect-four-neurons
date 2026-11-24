"""Neuron atlas data for the analysed model: one record per neuron with both poles, for the browsable atlas page.

Per pole (fires beyond p97 for +, below p3 for -): firing rate, mean ply, top-3 matching concepts with F1, how the board
differs when it fires (P(mine|fires) - P(mine) per cell, likewise theirs and empty), and its top activating positions.
Per neuron: activation quantiles, direct effect on the 7 column logits (through the unembedding, centred), and its causal
attribution for each tactic (results/tactic_attr.npz). Writes results/atlas/{meta,overview,games}.json and L<layer>.json.
"""
import json

import numpy as np
import torch

from c4n import analysis as A
from c4n import config, provenance
from c4n.concepts import FAMILY, INDEX, NAMES
from c4n.data import concepts_for, load_split
from c4n.model import load_checkpoint

CFG = config.load()
AC = CFG["analysis"]
DEV = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
CHUNK, N_EX, N_CAND = 512, 5, 40
OUT = config.results_dir(CFG) / "atlas"


def main():
    OUT.mkdir(exist_ok=True)
    model = load_checkpoint(config.ROOT / AC["checkpoint"], DEV)
    L, Fd = model.cfg["n_layer"], model.cfg["d_ff"]
    moves, _, lengths = load_split(CFG, "analysis")
    n = AC["n_games"]
    moves, lengths = moves[:n], lengths[:n]
    C = concepts_for(CFG, "analysis", n)
    gidx, tidx = A.valid_index(lengths)
    acts, _, _ = A.collect(model, moves, lengths, DEV)
    N = acts.shape[0]
    cc = C.sum(0)
    usable = (cc >= 50) & (cc <= N - 50)
    kidx = np.flatnonzero(usable)
    Cu = torch.as_tensor(C[:, kidx], dtype=torch.float32, device=DEV)
    cnt = Cu.sum(0)
    cell_idx = [INDEX[f"cell_r{r}c{c}_{s}"] for s in ("mine", "theirs", "empty") for r in range(6) for c in range(7)]  # 3 x 42
    Occ = torch.as_tensor(C[:, cell_idx], dtype=torch.float32, device=DEV)  # (N, 126)
    base = Occ.mean(0)
    tvec = torch.as_tensor(tidx, dtype=torch.float32, device=DEV)
    attr = np.load(config.results_dir(CFG) / "tactic_attr.npz")
    tactics = list(attr.files)
    # direct logit effect of each neuron through the final norm weight and the output head (centred over columns)
    W = model.head.weight.detach() @ (model.nf.w.detach()[:, None] * torch.stack([b.mlp.down.weight.detach() for b in model.blocks]).permute(1, 0, 2).reshape(model.cfg["d_model"], L * Fd))
    dle = (W - W.mean(0, keepdim=True)).T.reshape(L, Fd, 7).cpu().numpy()
    fams = sorted(set(FAMILY[k] for k in kidx))
    fam_id = {f: i for i, f in enumerate(fams)}
    games_used = set()
    ov = {"layer": [], "neuron": [], "sign": [], "c": [], "fam": [], "f1": [], "rate": [], "tac": []}
    for l in range(L):
        X_all = acts[:, l]
        recs = [{"n": j, "poles": [None, None]} for j in range(Fd)]
        for c0 in range(0, Fd, CHUNK):
            X = X_all[:, c0:c0 + CHUNK].to(DEV).float()
            c = X.shape[1]
            s = X.sort(0).values
            q = lambda p: s[min(N - 1, int(round(p / 100 * (N - 1))))]
            qs = {p: q(p) for p in (0.5, 3, 50, 97, 99.5)}
            top_val, top_idx = X.topk(N_CAND, 0)
            bot_val, bot_idx = (-X).topk(N_CAND, 0)
            for side, (fire, tv, ti) in enumerate(((X > qs[97], top_val, top_idx), (X < qs[3], bot_val, bot_idx))):
                f = fire.float()
                fc = f.sum(0).clamp_min(1)
                f1 = 2 * (f.T @ Cu) / (fc[:, None] + cnt[None, :])
                f1v, f1k = f1.topk(3, 1)
                occ = (f.T @ Occ) / fc[:, None] - base[None, :]  # (c, 126): how the board differs when it fires
                ply = (f.T @ tvec) / fc
                rate = f.mean(0)
                for j in range(c):
                    exs, seen = [], set()
                    for r in range(N_CAND):
                        p = int(ti[r, j])
                        g = int(gidx[p])
                        if g in seen:
                            continue
                        seen.add(g); games_used.add(g)
                        exs.append([g, int(tidx[p]), round(float(tv[r, j]) * (1 if side == 0 else -1), 2)])
                        if len(exs) == N_EX:
                            break
                    nj = c0 + j
                    recs[nj]["poles"][side] = {"s": "+-"[side], "thr": round(float(qs[97 if side == 0 else 3][j]), 3), "rate": round(float(rate[j]), 4), "ply": round(float(ply[j]), 1),
                                               "C": [int(kidx[k]) for k in f1k[j].tolist()], "F1": [round(float(v), 3) for v in f1v[j].tolist()],
                                               "occ": np.clip(np.round(occ[j].cpu().numpy() * 100), -100, 100).astype(int).tolist(), "ex": exs}
                    ov["layer"].append(l); ov["neuron"].append(nj); ov["sign"].append(side)
                    ov["c"].append(int(kidx[f1k[j, 0]]))
                    ov["fam"].append(fam_id[FAMILY[int(kidx[f1k[j, 0]])]]); ov["f1"].append(round(float(f1v[j, 0]), 3)); ov["rate"].append(round(float(rate[j]), 4))
                    ov["tac"].append([round(float(attr[t][l, nj]), 4) for t in tactics])
            for j in range(c):
                nj = c0 + j
                recs[nj]["q"] = [round(float(qs[p][j]), 3) for p in (0.5, 3, 50, 97, 99.5)]
                recs[nj]["dle"] = [round(float(v), 3) for v in dle[l, nj]]
                recs[nj]["tac"] = [round(float(attr[t][l, nj]), 4) for t in tactics]
        (OUT / f"L{l}.json").write_text(json.dumps(recs, separators=(",", ":")))
        print("layer", l, "done", flush=True)
    gm = {int(g): "".join(str(int(c)) for c in moves[g, : lengths[g]]) for g in sorted(games_used)}
    (OUT / "games.json").write_text(json.dumps(gm, separators=(",", ":")))
    (OUT / "overview.json").write_text(json.dumps(ov, separators=(",", ":")))
    meta = {"config": {k: CFG["model"][k] for k in ("n_layer", "d_model", "n_head", "d_ff")}, "concepts": [NAMES[k] for k in kidx], "families": fams,
            "tactics": tactics, "n_positions": int(N), "n_games": int(n), "fire_pct": AC["fire_pct"], "n_params": int(sum(p.numel() for p in model.parameters()))}
    (OUT / "meta.json").write_text(json.dumps(meta))
    provenance.write(OUT / "meta.json", CFG)
    print("atlas:", L * Fd, "neurons,", len(gm), "games referenced")


if __name__ == "__main__":
    main()
