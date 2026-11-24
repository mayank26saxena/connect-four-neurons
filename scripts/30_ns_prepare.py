"""Neuron Scientist, step 1 (PLAN.md addendum (q)): choose and blind the units, compute their dev firing thresholds, and cache
dev activations. Runs on CPU in a few minutes. Writes ns/units.json, ns/stats.json, ns/private/key.json, ns/cache/dev_acts.npy."""
import json

import numpy as np

from c4n import config
from c4n import ns

CFG = config.load()
NC = ns.ns_config(CFG)


def main():
    rng = np.random.default_rng(NC["seed"])
    model = ns.load_web_model()
    L, Fd = model.cfg["n_layer"], model.cfg["d_ff"]
    pt = json.loads((config.ROOT / "results" / "pole_table.json").read_text())
    f1 = np.array([r["f1_sweep"] for r in pt])
    if NC["exclude_key"]:  # (r) never re-describe a neuron from an earlier study
        prev = json.loads((config.ROOT / NC["exclude_key"]).read_text())
        used = {(v["layer"], v["neuron"]) for v in prev.values() if v["kind"] == "neuron"}
        f1 = np.where([(r["layer"], r["neuron"]) in used for r in pt], np.nan, f1)
    chosen = []
    expl = np.flatnonzero(f1 >= NC["explained_f1"])
    for i in rng.choice(expl, NC["n_explained"], replace=False):
        chosen.append(("explained", pt[i]))
    per_layer = NC["n_unexplained"] // L
    extra = NC["n_unexplained"] - per_layer * L
    for l in range(L):
        cand = [i for i in np.flatnonzero(f1 < NC["unexplained_f1"]) if pt[i]["layer"] == l]
        for i in rng.choice(cand, per_layer + (1 if l < extra else 0), replace=False):
            chosen.append(("unexplained", pt[i]))
    key = {}
    entries = []
    for stratum, r in chosen:
        entries.append({"kind": "neuron", "layer": int(r["layer"]), "neuron": int(r["neuron"]), "sign": 1 if r["pole"] == "+" else -1,
                        "stratum": stratum, "dict_concept_insample": r["concept_sweep"], "dict_f1_insample": float(r["f1_sweep"])})
    for j in range(NC["n_random"]):
        entries.append({"kind": "random_direction", "layer": int(j % L), "seed": int(NC["seed"] * NC.get("random_seed_mult", 100) + j), "sign": int(rng.choice([-1, 1])),
                        "stratum": "random"})
    order = rng.permutation(len(entries))
    units = []
    for k, idx in enumerate(order):
        uid = f"U{k + 1:02d}"
        key[uid] = entries[idx]
        units.append({"id": uid, "layer": entries[idx]["layer"], "pole": "+" if entries[idx]["sign"] > 0 else "-"})
    ns.PRIVATE.mkdir(parents=True, exist_ok=True); ns.CACHE.mkdir(parents=True, exist_ok=True)
    (ns.PRIVATE / "key.json").write_text(json.dumps(key, indent=1))
    (ns.NS / "units.json").write_text(json.dumps(units, indent=1))
    moves, _, lengths = ns.load_games(ns.DEV_SPLIT, NC["n_games"])
    us = [u["id"] for u in units]
    S = ns.unit_acts(model, moves, lengths, us, key).astype(np.float32)
    np.save(ns.CACHE / "dev_acts.npy", S)
    el = ns.eligible(lengths, NC["min_ply"])  # (r) thresholds and maxima over eligible positions only
    st = {}
    for j, u in enumerate(us):
        sign = key[u]["sign"]
        s = S[el, j]
        thr = float(np.percentile(s, NC["fire_pct"] if sign > 0 else 100 - NC["fire_pct"]))
        pole = sign * s
        st[u] = {"sign": sign, "thr": thr, "fire_rate": float(((s > thr) if sign > 0 else (s < thr)).mean()),
                 "dev_max_pole": float(pole.max()), "dev_max_raw": float(s[np.argmax(pole)]), "layer": key[u]["layer"],
                 "min_ply": int(NC["min_ply"])}
    (ns.NS / "stats.json").write_text(json.dumps(st, indent=1))
    print(f"{len(us)} units ({NC['n_explained']} explained, {NC['n_unexplained']} unexplained, {NC['n_random']} random directions), "
          f"{S.shape[0]:,} dev positions cached")


if __name__ == "__main__":
    main()
