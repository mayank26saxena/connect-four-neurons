"""PLAN.md addendum (t): what carries horizontal and diagonal blocking, if not a small set of neurons? Per threat orientation:
T1 neuron curve (the (s) rule restricted to layers 0-4, extended to 5,120 neurons), T2 subspace patching along the top singular
directions of the clean-minus-corrupted activation differences, random-subspace controls, T3 heads; predictions (t-1)-(t-5).
Everything is chosen on the discovery split (analysis) and reported on the confirmation split (val). Writes
results/orientation_followup.json. SMOKE=1: wiring check. Run on a GPU host."""
import json
import os
import time

import numpy as np
import torch
import torch.nn.functional as F

from c4n import circuit as C
from c4n import config, ns, provenance
from c4n import worldmodel as WM

CFG = config.load("circuit")
SMOKE = bool(os.environ.get("SMOKE"))
K = {**CFG, **(CFG["smoke"] if SMOKE else {})}
DEV = "cuda" if torch.cuda.is_available() else "cpu"
SEED = K["seed"]
OUT = config.results_dir(CFG) / ("orientation_followup_smoke.json" if SMOKE else "orientation_followup.json")
N_EXACT = 60 if SMOKE else 1000
KS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
N_RAND = 3 if SMOKE else 50
MAX_PER = 200 if SMOKE else 4000
ORS = C.ORIENT[:3]


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def neuron_ks(n_total):
    ks = list(range(1, 101)) + list(range(110, 1001, 10)) + list(range(1100, n_total + 1, 100))
    return sorted({k for k in ks if k <= n_total} | {n_total})


def t1_neurons(D, V, layers, target):
    """The (s) rule restricted to `layers`, with the curve extended to every neuron of those layers."""
    Fd = D.Fd
    attr = D.attribution()
    mask = np.full(attr.shape, -np.inf); mask[list(layers)] = 0
    a = (attr + mask).ravel()
    n_total = len(layers) * Fd
    top = np.argsort(-a)[:N_EXACT]
    exact = np.array([D.effect(D.run("clean", neurons=C.by_layer([f], Fd, D.dev), src="corr")) for f in top])
    pos = [int(top[i]) for i in np.argsort(-exact) if exact[i] > 0]
    seen = set(pos)
    rest = [int(f) for f in np.argsort(-a)[:n_total] if int(f) not in seen]
    order = pos + rest
    curve, n80 = [], None
    for k in neuron_ks(n_total):
        e = D.effect(D.run("clean", neurons=C.by_layer(order[:k], Fd, D.dev), src="corr"))
        curve.append([k, e])
        if e >= target:
            n80 = k
            break
    conf = V.effect(V.run("clean", neurons=C.by_layer(order[:n80], Fd, V.dev), src="corr")) if n80 else None
    return {"n80": n80, "curve": curve, "confirm_effect": conf, "n_exact_positive": len(pos),
            "layers_of_n80": {str(l): sum(1 for f in order[:n80 or 0] if f // Fd == l) for l in layers}}


def svd_dirs(D, layers):
    out, energy = {}, {}
    for l in layers:
        X = (D.acts["clean"][:, l] - D.acts["corr"][:, l]).float()
        _, S, Vh = torch.linalg.svd(X, full_matrices=False)
        out[l] = Vh  # rows = directions, by singular value
        e = (S ** 2) / (S ** 2).sum()
        energy[l] = torch.cumsum(e, 0).cpu().numpy()
    return out, energy


def t2_directions(D, V, layers, target, rng):
    dirs, energy = svd_dirs(D, layers)
    curve, k80 = [], None
    for k in KS:
        sub = {l: dirs[l][:k].T.contiguous() for l in layers}
        e = D.effect(D.run("clean", subspace=sub, src="corr"))
        curve.append([k * len(layers), e])
        if e >= target:
            k80 = k
            break
    res = {"d80": k80 * len(layers) if k80 else None, "k_per_layer": k80, "curve": curve,
           "energy_captured": {str(l): float(energy[l][(k80 or KS[-1]) - 1]) for l in layers}}
    if k80:
        sub = {l: dirs[l][:k80].T.contiguous() for l in layers}
        res["confirm_effect"] = V.effect(V.run("clean", subspace=sub, src="corr"))
        rnd = []
        for _ in range(N_RAND):
            rs = {}
            for l in layers:
                q, _ = torch.linalg.qr(torch.as_tensor(rng.standard_normal((D.Fd, k80)), dtype=torch.float32, device=D.dev))
                rs[l] = q
            rnd.append(V.effect(V.run("clean", subspace=rs, src="corr")))
        res["random_p50_p95"] = [float(np.percentile(rnd, 50)), float(np.percentile(rnd, 95))]
        # participation ratio of each direction over neurons (1 = one neuron, 1,024 = spread evenly)
        res["participation_ratio"] = {str(l): [float(1.0 / (dirs[l][j] ** 4).sum()) for j in range(k80)] for l in layers}
        res["_dirs"] = {l: dirs[l][:k80] for l in layers}
    return res


def t3_heads(D, V):
    single = {f"L{l}H{h}": V.effect(V.run("clean", heads=[(l, h)], src="corr")) for l in range(V.L) for h in range(V.H)}
    disc = {(l, h): D.effect(D.run("clean", heads=[(l, h)], src="corr")) for l in range(D.L) for h in range(D.H)}
    order = sorted(disc, key=lambda x: -disc[x])
    curve = [[m, V.effect(V.run("clean", heads=order[:m], src="corr"))] for m in range(1, 11)]
    top = max(single, key=single.get)
    return {"single_val": single, "top": top, "top_effect": single[top], "joint_curve_val": curve}


def direction_fields(model, dirs_by_o, Pt_by_o):
    """Receptive field (as in (s) S4) of the first direction of each layer, per orientation."""
    moves, _, lengths = ns.load_games("analysis", K["probe_games"])
    lab = WM.board_labels(moves, lengths)
    tr = lab["g"] < int(K["probe_train_frac"] * len(lengths))
    pts = [2 * l + 1 for l in range(5)]
    X = WM.collect_points(model, moves, lengths, DEV, pts)
    probes = {p: WM.fit_linear(X[torch.as_tensor(tr), i], lab["rel"][tr], 3, DEV, K["probe_steps"], K["probe_lr"], seed=SEED)
              for i, p in enumerate(pts)}
    del X
    out = {}
    for o, dirs in dirs_by_o.items():
        Pt = Pt_by_o[o]
        R = {p: [] for p in pts}
        with torch.no_grad():
            for sl, tt, ar in Pt._batches():
                _, kept = WM.run(model, Pt.tok["clean"][sl], keep=set(pts))
                for p in pts:
                    R[p].append(kept[p][ar, tt].float())
        out[o] = {}
        for l, Vh in dirs.items():
            p = 2 * l + 1
            x = torch.cat(R[p]).clone().requires_grad_(True)
            b = model.blocks[l]
            h = b.n2(x)
            a = F.silu(b.mlp.gate(h)) * b.mlp.up(h)
            u = Vh[0]
            mean_diff = (Pt.acts["clean"][:, l] - Pt.acts["corr"][:, l]).mean(0) @ u
            s = (a @ u) * torch.sign(mean_diff)
            gr = torch.autograd.grad(s.sum(), x)[0].mean(0)
            W = probes[p].W.to(gr.device)
            dm = W[:, :, WM.MINE] - W[:, :, WM.EMPTY]; dt = W[:, :, WM.THEIRS] - W[:, :, WM.EMPTY]
            dm, dt = dm / dm.norm(dim=0, keepdim=True), dt / dt.norm(dim=0, keepdim=True)
            out[o][str(l)] = {"mine": (gr @ dm).tolist(), "theirs": (gr @ dt).tolist()}
    model.zero_grad(set_to_none=True)
    return out


def main():
    t0 = time.time()
    torch.manual_seed(SEED)
    rng = np.random.default_rng(SEED)
    model = ns.load_web_model(DEV)
    P = {}
    for sp in ("analysis", "val"):
        mv, _, ln = ns.load_games(sp, K["n_games"])
        allp = C.block_pairs(mv, ln, SEED, 10 ** 7, K["min_stones"])
        for i, o in enumerate(ORS):
            idx = np.flatnonzero(allp["orient"] == i)
            if len(idx) > MAX_PER:
                idx = np.sort(rng.choice(idx, MAX_PER, replace=False))
            m = np.zeros(len(allp["t"]), dtype=bool); m[idx] = True
            P[(sp, o)] = C.Patcher(model, C.subset(allp, m), DEV, K["bs"])
    res = {"smoke": SMOKE, "n_pairs": {f"{sp}/{o}": P[(sp, o)].N for (sp, o) in P}, "gap": {f"{sp}/{o}": P[(sp, o)].gap for (sp, o) in P}}
    for scope, layers in (("layers0-4", range(5)), ("all_layers", range(6))):
        R = {}
        for o in ORS:
            D, V = P[("analysis", o)], P[("val", o)]
            allN = {l: torch.arange(D.Fd, device=DEV) for l in layers}
            e_d = D.effect(D.run("clean", neurons=allN, src="corr"))
            e_v = V.effect(V.run("clean", neurons=allN, src="corr"))
            target = 0.8 * e_d
            r = {"E_all_disc": e_d, "E_all_val": e_v, "target": target}
            r["T2"] = t2_directions(D, V, list(layers), target, rng)
            if scope == "layers0-4":
                r["T1"] = t1_neurons(D, V, list(layers), target)
                r["T3"] = t3_heads(D, V)
            R[o] = r
            log(scope, o, {"E_all": round(e_v, 3), "N80": r.get("T1", {}).get("n80"), "D80": r["T2"]["d80"]})
        res[scope] = R
    A = res["layers0-4"]
    n80 = {o: A[o]["T1"]["n80"] for o in ORS}
    d80 = {o: A[o]["T2"]["d80"] for o in ORS}
    pred = {}
    pred["t1"] = bool(n80["horizontal"] >= 3 * n80["vertical"] and n80["diagonal"] >= 3 * n80["vertical"])
    pred["t2"] = bool(all(d80[o] is not None and d80[o] <= 30 and A[o]["T2"]["confirm_effect"] >= 0.75 * A[o]["E_all_val"] for o in ORS))
    ratio = {o: (n80[o] / d80[o] if d80[o] else None) for o in ORS}
    pred["t3"] = bool(all(ratio[o] is not None for o in ORS) and ratio["horizontal"] > ratio["vertical"] and ratio["diagonal"] > ratio["vertical"])
    pred["t4"] = bool(all("random_p50_p95" in A[o]["T2"] and A[o]["T2"]["random_p50_p95"][1] <= 0.10 for o in ORS))
    th = {o: A[o]["T3"]["top_effect"] for o in ORS}
    pred["t5"] = bool(th["horizontal"] > th["vertical"] and th["diagonal"] > th["vertical"])
    res["summary"] = {"N80": n80, "D80": d80, "N80_over_D80": ratio, "top_head": {o: [A[o]["T3"]["top"], th[o]] for o in ORS},
                      "predictions_hold": pred}
    log("summary", res["summary"])
    dirs = {o: A[o]["T2"].pop("_dirs") for o in ORS if "_dirs" in A[o]["T2"]}
    for o in ORS:
        res["all_layers"][o]["T2"].pop("_dirs", None)
    res["direction_fields"] = direction_fields(model, dirs, {o: P[("analysis", o)] for o in dirs})
    res["seconds"] = round(time.time() - t0, 1)
    OUT.write_text(json.dumps(res, indent=1))
    provenance.write(OUT, {**K, "n_exact": N_EXACT, "ks": KS, "n_random": N_RAND, "max_per_orientation": MAX_PER})
    log(f"wrote {OUT} in {res['seconds']}s")


if __name__ == "__main__":
    main()
