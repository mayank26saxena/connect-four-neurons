"""Localise each tactic in the analysed model: components, neurons, information flow, attention. Writes tactic_atlas.json and
tactic_attr.npz (per-tactic neuron attribution, shape (L, F)). See PLAN.md addendum (f)."""
import json

import numpy as np
import torch

from c4n import config, provenance
from c4n import tactics as T
from c4n.data import load_split
from c4n.model import load_checkpoint

CFG = config.load()
AC, TC = CFG["analysis"], CFG["tactics"]
DEV = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")


def main():
    rng = np.random.default_rng(CFG["seed"])
    model = load_checkpoint(config.ROOT / AC["checkpoint"], DEV)
    L, Fd, Hh = model.cfg["n_layer"], model.cfg["d_ff"], model.cfg["n_head"]
    moves, scores, lengths = load_split(CFG, "analysis")
    n = AC["n_games"]
    moves, scores, lengths = moves[:n], scores[:n], lengths[:n]
    sets = T.tactic_sets(moves, lengths, TC["max_positions"], CFG["seed"])
    sets["control"] = T.control_set(moves, lengths, scores, TC["max_positions"], CFG["seed"])
    COLS = T.TACTICS + ["control"]
    out = {"tactics": T.TACTICS, "columns": COLS, "n_positions": {t: [len(s["idx"]), s["n_all"]] for t, s in sets.items()}}
    out["chance"] = {t: T.chance_rate(s) for t, s in sets.items()}
    intact = {t: T.rate(model, moves, s, DEV) for t, s in sets.items()}
    out["intact"] = intact
    print("intact", {t: round(v, 3) for t, v in intact.items()}, "chance", {t: round(v, 3) for t, v in out["chance"].items()}, flush=True)

    # ---- components: mean-ablate each MLP and each head ----
    mean_a, mean_y = T.means(model, moves, lengths, DEV)
    comps, heat = [], []
    for l in range(L):
        comps.append({"layer": l, "kind": "mlp", "name": f"L{l} MLP"})
        heat.append([intact[t] - T.rate(model, moves, sets[t], DEV, hook=T.mlp_mean_hook(l, mean_a)) for t in COLS])
        for h in range(Hh):
            comps.append({"layer": l, "kind": "head", "head": h, "name": f"L{l} H{h}"})
            heat.append([intact[t] - T.rate(model, moves, sets[t], DEV, attn_hook=T.head_mean_hook(l, h, mean_y)) for t in COLS])
    out["components"], out["component_drop"] = comps, heat
    print("components done", flush=True)

    # ---- neuron attribution + validation against random neurons ----
    attr, val = {}, {}
    for t in T.TACTICS:
        a, npos = T.attribution(model, moves, sets[t], DEV)
        attr[t] = a / npos
        flat = np.argsort(-a.reshape(-1))  # most supportive first
        val[t] = []
        for k in TC["topk"]:
            top = flat[:k]
            by_layer = {l: (top[(top // Fd) == l] % Fd).tolist() for l in range(L)}
            top_rate = T.rate(model, moves, sets[t], DEV, hook=T.neuron_zero_hook(by_layer))
            top_ctrl = T.rate(model, moves, sets["control"], DEV, hook=T.neuron_zero_hook(by_layer))  # general damage
            rnd, rnd_ctrl = [], []
            for _ in range(TC["n_random"]):
                rb = {l: rng.choice(Fd, len(v), replace=False).tolist() for l, v in by_layer.items()}
                rnd.append(T.rate(model, moves, sets[t], DEV, hook=T.neuron_zero_hook(rb)))
                rnd_ctrl.append(T.rate(model, moves, sets["control"], DEV, hook=T.neuron_zero_hook(rb)))
            val[t].append({"k": k, "top_rate": top_rate, "control_rate_top": top_ctrl, "random_rate_mean": float(np.mean(rnd)),
                           "control_rate_random": float(np.mean(rnd_ctrl)), "random_rate_min": float(np.min(rnd)),
                           "layers": {str(l): len(v) for l, v in by_layer.items() if v}})
        top = flat[:50]
        out.setdefault("top_neurons", {})[t] = [{"layer": int(i // Fd), "neuron": int(i % Fd), "score": float(a.reshape(-1)[i] / npos)} for i in top]
        print(t, "validation", [(v["k"], round(v["top_rate"], 3), round(v["random_rate_mean"], 3)) for v in val[t]], flush=True)
    out["neuron_validation"] = val
    np.savez_compressed(config.results_dir(CFG) / "tactic_attr.npz", **{t: attr[t].astype(np.float32) for t in T.TACTICS})

    # ---- decodability: probes on the residual stream, all positions, held out by game ----
    pos, mask = T.boards(moves, lengths)
    m = T.tactic_masks(pos, mask)
    win = m["win"].any(1)
    block = ~win & m["block"].any(1)
    poison = ~win & ~block & (m["poison"].any(1))
    fork = m["fork"].any(1)
    labels = {"win": win, "block": block, "poison": poison, "fork": fork}
    g_all, _ = T.position_index(lengths)
    train = g_all < int(TC["probe_train_frac"] * n)
    res = T.residuals(model, moves, lengths, DEV)
    out["probe_auroc"] = {t: [T.probe_auroc(res[:, i], labels[t].astype(np.int8), train, DEV, TC["probe_steps"]) for i in range(L + 1)] for t in T.TACTICS}
    out["probe_base_rate"] = {t: float(labels[t].mean()) for t in T.TACTICS}
    print("probes", {t: [round(x, 2) for x in v] for t, v in out["probe_auroc"].items()}, flush=True)

    # ---- attention profiles at the deciding position ----
    out["attention_profile"] = {t: T.attention_profile(model, moves, sets[t], DEV).round(4).tolist() for t in T.TACTICS}
    path = config.results_dir(CFG) / "tactic_atlas.json"
    path.write_text(json.dumps(out))
    provenance.write(path, CFG)


if __name__ == "__main__":
    main()
