"""Test B, step 1 (PLAN.md addendum (s), S7): choose and blind the units for study (s) from the FROZEN circuit.
Units: the top-n circuit poles by exact effect, one matched decoy per circuit pole, and n_random random directions, shuffled behind
opaque ids. Decoy = a pole (same sign) of a neuron in the same layer, outside the top 1,000 of the attribution ranking, not in the
circuit and never described in (q)/(r), nearest on standardised (log p97 pole magnitude, activation kurtosis), estimated on the
first `stat_games` dev games (>= 4 stones). Circuit membership is written to results/ns3_membership.json, which is NOT part of the
agent bundle (scripts/38_ns3_bundle.py); the key in ns3/private/ only says neuron or random direction.
Then, exactly as scripts/30_ns_prepare.py: dev thresholds (p97 / p3 over eligible positions) and the dev activation cache.
Run with C4N_CONFIG=ns3 NS_DIR=ns3 on a GPU host."""
import json

import numpy as np
import torch

from c4n import config, ns
from c4n.model import tokens_from_moves

CFG = config.load()
NC = ns.ns_config(CFG)
ROOT = config.ROOT
DEV = "cuda" if torch.cuda.is_available() else "cpu"


@torch.no_grad()
def neuron_stats(model, moves, lengths, min_ply):
    """Per neuron (L, F): p97 and p3 of the raw activation and its kurtosis, over eligible dev positions."""
    L, Fd = model.cfg["n_layer"], model.cfg["d_ff"]
    acts = [[] for _ in range(L)]
    for i in range(0, len(lengths), 256):
        tok = tokens_from_moves(torch.as_tensor(moves[i:i + 256])).to(DEV)
        ln = torch.as_tensor(lengths[i:i + 256], device=DEV)
        ar = torch.arange(42, device=DEV)[None]
        ok = (ar < ln[:, None]) & (ar >= min_ply)

        def hook(l, a, g, u):
            acts[l].append(a[:, :42][ok].half().cpu()); return a
        model(tok, hook=hook)
    p97, p3, kurt = (np.zeros((L, Fd)) for _ in range(3))
    for l in range(L):
        A = torch.cat(acts[l]).float().to(DEV)
        for c in range(0, Fd, 128):
            x = A[:, c:c + 128]
            q = torch.quantile(x, torch.tensor([0.03, 0.97], device=DEV), dim=0)
            p3[l, c:c + 128], p97[l, c:c + 128] = q[0].cpu().numpy(), q[1].cpu().numpy()
            z = (x - x.mean(0)) / x.std(0).clamp_min(1e-8)
            kurt[l, c:c + 128] = (z ** 4).mean(0).cpu().numpy()
        del A
    return p97, p3, kurt


def main():
    rng = np.random.default_rng(NC["seed"])
    model = ns.load_web_model(DEV)
    L, Fd = model.cfg["n_layer"], model.cfg["d_ff"]
    circ = json.loads((ROOT / "results" / "block_circuit.json").read_text())
    assert not circ["smoke"], "use the frozen full-run circuit"
    top = circ["circuit"]["neurons"][: NC["n_circuit"]]
    attr1000 = set(circ["circuit"]["attr_rank_top1000"])
    cset = {n["id"] for n in circ["circuit"]["neurons"]}
    described = set()
    for ws in ("ns", "ns2"):
        for r in json.loads((ROOT / ws / "report.json").read_text())["rows"]:
            if r["kind"] == "neuron":
                described.add(r["layer"] * Fd + r["neuron"])
    moves, _, lengths = ns.load_games(ns.DEV_SPLIT, NC["stat_games"])
    p97, p3, kurt = neuron_stats(model, moves, lengths, NC["min_ply"])
    used, decoys = set(), []
    for n in top:
        l, sgn = n["layer"], 1 if n["pole"] == "+" else -1
        mag = np.log(np.maximum(1e-6, p97[l] if sgn > 0 else -p3[l]))
        feats = np.stack([mag, np.log(np.maximum(kurt[l], 1e-6))], 1)
        feats = (feats - feats.mean(0)) / feats.std(0)
        ok = np.array([(l * Fd + j) not in attr1000 | cset | described | used for j in range(Fd)])
        d = np.where(ok, np.linalg.norm(feats - feats[n["neuron"]], axis=1), np.inf)
        j = int(np.argmin(d))
        used.add(l * Fd + j)
        decoys.append({"layer": l, "neuron": j, "pole": n["pole"], "matched_to": n["id"], "distance": float(d[j]),
                       "log_mag": [float(mag[n["neuron"]]), float(mag[j])], "kurtosis": [float(kurt[l, n["neuron"]]), float(kurt[l, j])]})
    entries = []
    for n in top:
        entries.append(({"kind": "neuron", "layer": n["layer"], "neuron": n["neuron"], "sign": 1 if n["pole"] == "+" else -1, "stratum": "blind"},
                        {"group": "circuit", "rank": n["rank"], "exact_effect": n["exact_effect"]}))
    for dcy in decoys:
        entries.append(({"kind": "neuron", "layer": dcy["layer"], "neuron": dcy["neuron"], "sign": 1 if dcy["pole"] == "+" else -1, "stratum": "blind"},
                        {"group": "decoy", **dcy}))
    for j in range(NC["n_random"]):
        entries.append(({"kind": "random_direction", "layer": int(j % L), "seed": int(NC["seed"] * NC["random_seed_mult"] + j),
                         "sign": int(rng.choice([-1, 1])), "stratum": "random"}, {"group": "random"}))
    order = rng.permutation(len(entries))
    key, units, member = {}, [], {}
    for k, idx in enumerate(order):
        uid = f"U{k + 1:02d}"
        key[uid], member[uid] = entries[idx]
        units.append({"id": uid, "layer": key[uid]["layer"], "pole": "+" if key[uid]["sign"] > 0 else "-"})
    ns.PRIVATE.mkdir(parents=True, exist_ok=True); ns.CACHE.mkdir(parents=True, exist_ok=True)
    (ns.PRIVATE / "key.json").write_text(json.dumps(key, indent=1))
    (ns.NS / "units.json").write_text(json.dumps(units, indent=1))
    (ROOT / "results" / "ns3_membership.json").write_text(json.dumps({"circuit_sha256_note": "see docs/LOG.md (S5 freeze)",
                                                                       "units": member}, indent=1))
    # as scripts/30_ns_prepare.py: dev cache and thresholds over eligible positions
    moves, _, lengths = ns.load_games(ns.DEV_SPLIT, NC["n_games"])
    us = [u["id"] for u in units]
    model_cpu = model.cpu()
    S = ns.unit_acts(model_cpu, moves, lengths, us, key).astype(np.float32)
    np.save(ns.CACHE / "dev_acts.npy", S)
    el = ns.eligible(lengths, NC["min_ply"])
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
    print(f"{len(us)} units ({len(top)} circuit, {len(decoys)} decoys, {NC['n_random']} random directions); "
          f"decoy match distance median {np.median([d['distance'] for d in decoys]):.2f}")


if __name__ == "__main__":
    main()
