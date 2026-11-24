"""Q2/Q3: match every neuron pole to ground-truth concepts, against a random-direction baseline.

For each pole (layer, neuron, sign) and each binary concept: F1 of "pole fires" vs "concept is true", (a) at the
p97/p3 firing threshold used by Tigges et al. and (b) best over a sweep of thresholds. The same is computed for random
orthogonal rotations of each layer's activation space. Pole independence (Q2): how often the two poles of one neuron
match the same concept / concept family, against randomly paired poles.

Writes results/concepts_summary.json and results/pole_table.json (one row per pole, used by the blog and demo).
"""
import json

import numpy as np
import torch

from c4n import analysis as A
from c4n import config, provenance
from c4n.concepts import FAMILY, NAMES
from c4n.data import concepts_for, load_split
from c4n.model import load_checkpoint

CFG = config.load()
AC = CFG["analysis"]
DEV = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
FIRE = AC["fire_pct"]


def summarise(res, label):
    out = {}
    for key, arr in (("f1_p%d" % FIRE, res["f1_at"][FIRE]), ("f1_sweep", res["f1_sweep"])):
        L = arr.shape[0]
        out[key] = {
            "median": float(np.median(arr)),
            "share_ge_0.5": float((arr >= 0.5).mean()),
            "share_ge_0.8": float((arr >= 0.8).mean()),
            "by_layer_median": [float(np.median(arr[l])) for l in range(L)],
            "by_layer_share_ge_0.5": [float((arr[l] >= 0.5).mean()) for l in range(L)],
            "hist": np.histogram(arr, bins=20, range=(0, 1))[0].tolist(),
        }
    out["label"] = label
    return out


TRIVIAL = {"ply", "me_first_player", "last_col"}  # readable straight from position / current-token embeddings


def family_table(res):
    """Per concept family: best pole F1 (sweep), poles whose best concept is in the family, and how many reach F1 >= 0.5 / 0.8."""
    f1, arg = res["f1_sweep"].reshape(-1), res["arg_sweep"].reshape(-1)
    fam_of_pole = np.array([FAMILY[k] for k in arg])
    out = {}
    for fam in sorted(set(FAMILY[k] for k in res["concept_index"])):
        m = fam_of_pole == fam
        out[fam] = {"trivial": fam in TRIVIAL, "n_poles_best": int(m.sum()),
                    "n_ge_0.5": int((f1[m] >= 0.5).sum()), "n_ge_0.8": int((f1[m] >= 0.8).sum()),
                    "best_f1": float(f1[m].max()) if m.any() else None}
    return out


def pole_independence(arg, rng):
    """Share of neurons whose two poles match the same concept / family; baseline pairs poles of random neurons."""
    L, Fd, _ = arg.shape
    same = (arg[..., 0] == arg[..., 1]).mean()
    fam = np.vectorize(lambda k: FAMILY[k])
    fpos, fneg = fam(arg[..., 0]), fam(arg[..., 1])
    same_fam = (fpos == fneg).mean()
    perm = rng.permutation(L * Fd)
    neg_shuf = arg[..., 1].reshape(-1)[perm].reshape(L, Fd)
    base = (arg[..., 0] == neg_shuf).mean()
    base_fam = (fpos == fam(neg_shuf)).mean()
    return {"same_concept": float(same), "same_concept_shuffled": float(base),
            "same_family": float(same_fam), "same_family_shuffled": float(base_fam)}


def main():
    rng = np.random.default_rng(CFG["seed"])
    model = load_checkpoint(config.ROOT / AC["checkpoint"], DEV)
    moves, scores, lengths = load_split(CFG, "analysis")
    n = AC["n_games"]
    C = concepts_for(CFG, "analysis", n)
    acts, _, _ = A.collect(model, moves[:n], lengths[:n], DEV)
    neur = A.pole_concept_scores(acts, C, DEV)
    rot = A.pole_concept_scores(acts, C, DEV, rotation=A.random_rotations(acts.shape[1], acts.shape[2], AC["rotation_seed"], DEV))
    hi, lo = A.percentiles(acts, [FIRE, 100 - FIRE], DEV)
    summary = {"n_positions": int(acts.shape[0]), "n_concepts_used": int(len(neur["concept_index"])),
               "neurons": summarise(neur, "neuron basis"), "random_rotation": summarise(rot, "random rotation"),
               "families_neurons": family_table(neur), "families_random_rotation": family_table(rot),
               "pole_independence_p%d" % FIRE: pole_independence(neur["arg_at"][FIRE], rng),
               "concept_base_rate": {NAMES[k]: float(C[:, k].mean()) for k in neur["concept_index"]}}
    rows = []
    L, Fd, _ = neur["f1_sweep"].shape
    for l in range(L):
        for f in range(Fd):
            for s, sign in enumerate("+-"):
                rows.append({"layer": l, "neuron": f, "pole": sign,
                             "threshold": float(hi[l, f] if s == 0 else lo[l, f]),
                             "concept_p%d" % FIRE: NAMES[neur["arg_at"][FIRE][l, f, s]],
                             "f1_p%d" % FIRE: round(float(neur["f1_at"][FIRE][l, f, s]), 4),
                             "concept_sweep": NAMES[neur["arg_sweep"][l, f, s]],
                             "f1_sweep": round(float(neur["f1_sweep"][l, f, s]), 4),
                             "sweep_pct": float(neur["pct_sweep"][l, f, s])})
    res = config.results_dir(CFG)
    (res / "concepts_summary.json").write_text(json.dumps(summary, indent=1))
    (res / "pole_table.json").write_text(json.dumps(rows))
    provenance.write(res / "concepts_summary.json", CFG)
    provenance.write(res / "pole_table.json", CFG)
    for k in ("neurons", "random_rotation"):
        s = summary[k]
        print(k, {m: (round(s[m]["median"], 3), round(s[m]["share_ge_0.5"], 3), round(s[m]["share_ge_0.8"], 3)) for m in ("f1_p%d" % FIRE, "f1_sweep")})
    print(summary["pole_independence_p%d" % FIRE])
    top = sorted(rows, key=lambda r: -r["f1_sweep"])[:25]
    for r in top:
        print(r["layer"], r["neuron"], r["pole"], r["concept_sweep"], r["f1_sweep"])


if __name__ == "__main__":
    main()
