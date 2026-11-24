"""Q6: when do concepts get neurons, relative to when the model acts on them?

For every saved checkpoint: (a) behaviour on the analysis positions: take-win rate (a winning move is available and
the greedy legal move wins), block rate (the opponent threatens, no win is available, and the move blocks), agreement
with the teacher's best move, KL to the final checkpoint; (b) per concept family, the best pole F1 (threshold sweep)
and the number of poles with F1 >= 0.5; (c) for a fixed list of tracked concepts, the best pole F1.
Writes results/dynamics.json.
"""
import json

import numpy as np
import torch

from c4n import analysis as A
from c4n import config, provenance
from c4n.concepts import FAMILY, INDEX, NAMES
from c4n.data import concepts_for, flat_scores, load_split
from c4n.model import load_checkpoint

CFG = config.load()
AC, DC = CFG["analysis"], CFG["dynamics"]
DEV = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")


def behaviour(logits, C, scores):
    legal = torch.as_tensor(scores) != -32768
    pick = logits.masked_fill(~legal, -1e9).argmax(-1).numpy()
    win = np.stack([C[:, INDEX[f"win_now_c{c}"]] for c in range(7)], 1)
    blk = np.stack([C[:, INDEX[f"block_now_c{c}"]] for c in range(7)], 1)
    r = np.arange(len(pick))
    has_win, has_blk = win.any(1), blk.any(1) & ~win.any(1)
    return {"take_win_rate": float(win[r, pick][has_win].mean()), "block_rate": float(blk[r, pick][has_blk].mean()),
            "n_win_positions": int(has_win.sum()), "n_block_positions": int(has_blk.sum())}


def main():
    moves, scores, lengths = load_split(CFG, "analysis")
    n = DC["n_games"]
    moves, scores, lengths = moves[:n], scores[:n], lengths[:n]
    C = concepts_for(CFG, "analysis", n)
    fs = flat_scores(scores, lengths)
    ck_dir = config.ROOT / CFG["train"]["out_dir"]
    steps = CFG["train"]["ckpt_steps"]
    final = load_checkpoint(ck_dir / f"step_{steps[-1]:06d}.pt", DEV)
    _, _, ref = A.collect(final, moves, lengths, DEV)
    rows = []
    for st in steps:
        model = load_checkpoint(ck_dir / f"step_{st:06d}.pt", DEV)
        acts, _, lg = A.collect(model, moves, lengths, DEV)
        m = A.policy_metrics(lg, ref, fs)
        rec = {"step": st, "kl_to_final": m["kl"], "agree_teacher": m["agree"], **behaviour(lg, C, fs)}
        res = A.pole_concept_scores(acts, C, DEV, thresholds_pct=(97,))
        f1, arg = res["f1_sweep"].reshape(-1), res["arg_sweep"].reshape(-1)
        fam = np.array([FAMILY[k] for k in arg])
        rec["families"] = {f: {"best_f1": float(f1[fam == f].max()) if (fam == f).any() else 0.0,
                               "n_ge_0.5": int((f1[fam == f] >= 0.5).sum())} for f in sorted(set(FAMILY))}
        rec["tracked"] = {}
        for name in DC["tracked_concepts"]:
            hit = arg == INDEX[name]
            rec["tracked"][name] = float(f1[hit].max()) if hit.any() else 0.0
        rows.append(rec)
        print(json.dumps({k: v for k, v in rec.items() if k not in ("families", "tracked")}), flush=True)
    path = config.results_dir(CFG) / "dynamics.json"
    path.write_text(json.dumps({"n_games": n, "checkpoints": rows}, indent=1))
    provenance.write(path, CFG)


if __name__ == "__main__":
    main()
