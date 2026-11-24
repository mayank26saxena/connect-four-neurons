"""Q5: do concept-matched poles cause the behaviour their concept implies?

Action concepts name a column c: win_now_c (playing c wins), block_now_c (the opponent wins at c unless blocked),
poison_c (playing c lets the opponent win on top), teacher_best_c. For every pole whose best concept (threshold sweep)
is one of these with F1 >= `min_f1`:
- necessity: on positions where the concept holds, the rate at which the model's greedy legal move is c, intact vs with
  the neuron zeroed at every position, vs zeroing `n_random` random neurons of the same layer (one at a time);
- sufficiency: on positions where the concept does not hold, the rate of playing c intact vs with the neuron clamped
  to its pole's `clamp_pct` percentile at the evaluated position only.
Writes results/action.json.
"""
import json
import re

import numpy as np
import torch

from c4n import analysis as A
from c4n import config, provenance
from c4n.concepts import INDEX
from c4n.data import concepts_for, load_split
from c4n.model import load_checkpoint, tokens_from_moves

CFG = config.load()
AC, QC = CFG["analysis"], CFG["action"]
DEV = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
PAT = re.compile(r"^(win_now|block_now|poison|teacher_best)_c(\d)$")


@torch.no_grad()
def play_rate(model, moves, legal_all, games, ts, col, hook_fn=None, bs=1024):
    """Fraction of (game, t) positions where the greedy legal move is `col`. hook_fn(tt) builds a hook per batch."""
    hits = 0
    for i in range(0, len(games), bs):
        g, t = games[i:i + bs], ts[i:i + bs]
        tok = tokens_from_moves(torch.as_tensor(moves[g])).to(DEV)
        tt = torch.as_tensor(t, device=DEV)
        lg = model(tok, hook=None if hook_fn is None else hook_fn(tt))
        lg = lg[torch.arange(len(g), device=DEV), tt]
        legal = torch.as_tensor(legal_all[g, t], device=DEV)
        hits += (lg.masked_fill(~legal, -1e9).argmax(-1) == col).sum().item()
    return hits / max(1, len(games))


def zero_all(layer, neuron):
    return lambda tt: A.neuron_hook(layer, neuron, lambda a, g, u: torch.zeros_like(a))


def clamp_at(layer, neuron, value):
    def build(tt):
        def hook(l, a, g, u):
            if l != layer:
                return a
            a = a.clone()
            a[torch.arange(a.shape[0], device=a.device), tt, neuron] = value
            return a
        return hook
    return build


def main():
    rng = np.random.default_rng(CFG["seed"])
    model = load_checkpoint(config.ROOT / AC["checkpoint"], DEV)
    moves, scores, lengths = load_split(CFG, "analysis")
    n = AC["n_games"]
    moves, lengths = moves[:n], lengths[:n]
    C = concepts_for(CFG, "analysis", n)
    gidx, tidx = A.valid_index(lengths)
    oh = np.zeros(moves.shape + (7,), dtype=np.int16)
    gg, tt = np.nonzero(moves >= 0)
    oh[gg, tt, moves[gg, tt]] = 1
    legal_all = (np.cumsum(oh, 1) - oh) < 6
    acts, _, _ = A.collect(model, moves, lengths, DEV)
    clampv = A.percentiles(acts, [QC["clamp_pct"], 100 - QC["clamp_pct"]], DEV)
    rows = json.loads((config.results_dir(CFG) / "pole_table.json").read_text())
    cand = [r for r in rows if PAT.match(r["concept_sweep"]) and r["f1_sweep"] >= QC["min_f1"]]
    cand.sort(key=lambda r: -r["f1_sweep"])
    cand = cand[:QC["max_poles"]]
    d_ff = CFG["model"]["d_ff"]
    out = []
    for r in cand:
        fam, col = PAT.match(r["concept_sweep"]).groups()
        col = int(col)
        k = INDEX[r["concept_sweep"]]
        pos_t = np.flatnonzero(C[:, k])
        pos_f = np.flatnonzero(~C[:, k] & legal_all[gidx, tidx, col])
        pos_t = rng.choice(pos_t, min(len(pos_t), QC["max_positions"]), replace=False)
        pos_f = rng.choice(pos_f, min(len(pos_f), QC["max_positions"]), replace=False)
        l, nn = r["layer"], r["neuron"]
        rec = {"layer": l, "neuron": nn, "pole": r["pole"], "concept": r["concept_sweep"], "f1": r["f1_sweep"],
               "n_true": int(len(pos_t)), "n_false": int(len(pos_f))}
        rec["true_intact"] = play_rate(model, moves, legal_all, gidx[pos_t], tidx[pos_t], col)
        rec["true_ablated"] = play_rate(model, moves, legal_all, gidx[pos_t], tidx[pos_t], col, zero_all(l, nn))
        rand = [play_rate(model, moves, legal_all, gidx[pos_t], tidx[pos_t], col, zero_all(l, int(j)))
                for j in rng.choice([j for j in range(d_ff) if j != nn], QC["n_random"], replace=False)]
        rec["true_random_ablated_mean"] = float(np.mean(rand))
        rec["true_random_ablated_min"] = float(np.min(rand))
        v = float(clampv[0 if r["pole"] == "+" else 1, l, nn]) * QC["clamp_scale"]
        rec["clamp_value"] = v
        rec["false_intact"] = play_rate(model, moves, legal_all, gidx[pos_f], tidx[pos_f], col)
        rec["false_clamped"] = play_rate(model, moves, legal_all, gidx[pos_f], tidx[pos_f], col, clamp_at(l, nn, v))
        out.append(rec)
        print(json.dumps({k2: (round(x, 3) if isinstance(x, float) else x) for k2, x in rec.items()}), flush=True)
    path = config.results_dir(CFG) / "action.json"
    path.write_text(json.dumps({"n_candidates": len(cand), "poles": out}, indent=1))
    provenance.write(path, CFG)


if __name__ == "__main__":
    main()
