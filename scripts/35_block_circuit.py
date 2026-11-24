"""Blocking circuit (PLAN.md addendum (s), S0-S4): minimal pairs, component and neuron patching, the pre-registered circuit
rule, faithfulness tests (s-1)-(s-6) on the confirmation split, and descriptive mechanism maps (receptive fields, direct logit
effects). Writes results/block_circuit.json (+ .meta.json). Model: the float16 web export, the weights the describing agents use.
SMOKE=1: tiny wiring check (numbers meaningless). Run on a GPU host."""
import json
import os
import time

import numpy as np
import torch
import torch.nn.functional as F

from c4n import circuit as C
from c4n import config, ns, provenance
from c4n import tactics as T
from c4n import worldmodel as WM
from c4n.model import tokens_from_moves

CFG = config.load("circuit")
SMOKE = bool(os.environ.get("SMOKE"))
K = {**CFG, **(CFG["smoke"] if SMOKE else {})}
DEV = "cuda" if torch.cuda.is_available() else "cpu"
SEED = K["seed"]
OUT = config.results_dir(CFG) / ("block_circuit_smoke.json" if SMOKE else "block_circuit.json")


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def pair_summary(P, Pt):
    pc, pr = Pt.pick["clean"], Pt.pick["corr"]
    return {"n_candidates": P["n_candidates"], "n_with_pair": P["n_with_pair"], "n_pairs": int(Pt.N),
            "orient_counts": {o: int((P["orient"] == i).sum()) for i, o in enumerate(C.ORIENT)},
            "clean_block_acc": float((pc == P["block_col"]).mean()), "corr_plays_block_col": float((pr == P["block_col"]).mean()),
            "margin_clean": float(Pt.base["clean"].mean()), "margin_corr": float(Pt.base["corr"].mean()), "gap": Pt.gap}


def components(Pt):
    heads = {f"L{l}H{h}": Pt.effect(Pt.run("clean", heads=[(l, h)], src="corr")) for l in range(Pt.L) for h in range(Pt.H)}
    allN = torch.arange(Pt.Fd, device=Pt.dev)
    mlps = {f"L{l} MLP": Pt.effect(Pt.run("clean", neurons={l: allN}, src="corr")) for l in range(Pt.L)}
    return {"heads": heads, "mlps": mlps}


def ratio_ci(Pt, mg, groups, kind="effect"):
    c, r = Pt.base["clean"], Pt.base["corr"]
    if kind == "effect":
        f = lambda ix: (c[ix].mean() - mg[ix].mean()) / (c[ix].mean() - r[ix].mean())
    else:
        f = lambda ix: (mg[ix].mean() - r[ix].mean()) / (c[ix].mean() - r[ix].mean())
    return C.boot(f, groups, K["n_boot"], SEED)


def random_matched(circ, Fd, rng, exclude):
    """A random neuron set with the same number of neurons per layer as `circ`, avoiding `exclude`."""
    out = []
    for l, ix in C.by_layer(circ, Fd, "cpu").items():
        pool = np.setdiff1d(np.arange(l * Fd, (l + 1) * Fd), np.array(sorted(exclude)))
        out += list(rng.choice(pool, len(ix), replace=False))
    return out


def mean_hook(circ, mean_a, Fd):
    ix = C.by_layer(circ, Fd, "cpu")

    def hook(l, a, g, u):
        if l not in ix:
            return a
        a = a.clone(); j = ix[l].to(a.device)
        a[..., j] = mean_a[l][j.cpu()].to(a.device)
        return a
    return hook


def receptive_fields(model, circ, poles, Pt, Fd):
    """Gradient of each circuit neuron's pole activation w.r.t. the residual at its input (after its layer's attention),
    averaged over the clean last positions, projected on unit board-probe directions (mine - empty, theirs - empty) per cell."""
    moves, _, lengths = ns.load_games("analysis", K["probe_games"])
    lab = WM.board_labels(moves, lengths)
    tr = lab["g"] < int(K["probe_train_frac"] * len(lengths))
    layers = sorted({f // Fd for f in circ})
    pts = [2 * l + 1 for l in layers]
    X = WM.collect_points(model, moves, lengths, DEV, pts)
    probes, acc = {}, {}
    for i, p in enumerate(pts):
        Pr = WM.fit_linear(X[torch.as_tensor(tr), i], lab["rel"][tr], 3, DEV, K["probe_steps"], K["probe_lr"], seed=SEED)
        pred = WM.predict(Pr.logits, X[torch.as_tensor(~tr), i], DEV)
        acc[p] = float((pred == lab["rel"][~tr]).mean())
        probes[p] = Pr
    del X
    # residual at each needed point, last position of every clean pair
    R = {p: [] for p in pts}
    with torch.no_grad():
        for sl, tt, ar in Pt._batches():
            _, kept = WM.run(model, Pt.tok["clean"][sl], keep=set(pts))
            for p in pts:
                R[p].append(kept[p][ar, tt].float())
    R = {p: torch.cat(v) for p, v in R.items()}
    out = {}
    for f in circ:
        l, n = divmod(f, Fd)
        p = 2 * l + 1
        x = R[p].clone().requires_grad_(True)
        b = model.blocks[l]
        h = b.n2(x)
        a = F.silu(b.mlp.gate(h)[:, n]) * b.mlp.up(h)[:, n]
        gr = torch.autograd.grad(a.sum(), x)[0].mean(0) * poles[f]
        W = probes[p].W.to(gr.device)  # (d, 42, 3)
        dm = W[:, :, WM.MINE] - W[:, :, WM.EMPTY]; dt = W[:, :, WM.THEIRS] - W[:, :, WM.EMPTY]
        dm, dt = dm / dm.norm(dim=0, keepdim=True), dt / dt.norm(dim=0, keepdim=True)
        out[f] = {"mine": (gr @ dm).tolist(), "theirs": (gr @ dt).tolist(), "grad_norm": float(gr.norm())}
    model.zero_grad(set_to_none=True)
    return out, {f"point{p}": a for p, a in acc.items()}


def direct_logit(model, f, Fd):
    l, n = divmod(f, Fd)
    w = model.blocks[l].mlp.down.weight[:, n] * model.nf.w
    v = (model.head.weight @ w).detach().cpu().numpy()
    return (v - v.mean()).tolist()  # centred: only differences between columns matter for the move


def main():
    t0 = time.time()
    torch.manual_seed(SEED)
    rng = np.random.default_rng(SEED)
    model = ns.load_web_model(DEV)
    Fd = model.cfg["d_ff"]
    data = {sp: ns.load_games(sp, K["n_games"]) for sp in ("analysis", "val")}
    pairs, Pt = {}, {}
    for sp, (mv, sc, ln) in data.items():
        pairs[sp] = C.block_pairs(mv, ln, SEED, K["max_pairs"], K["min_stones"])
        Pt[sp] = C.Patcher(model, pairs[sp], DEV, K["bs"])
        log(sp, pair_summary(pairs[sp], Pt[sp]))
    D, V = Pt["analysis"], Pt["val"]
    res = {"smoke": SMOKE, "config": K, "pairs": {sp: pair_summary(pairs[sp], Pt[sp]) for sp in pairs}}

    # S1 components (both splits; predictions read on the confirmation split)
    res["components"] = {sp: components(Pt[sp]) for sp in Pt}
    log("components done")

    # S2 the circuit rule (discovery split)
    fc = C.find_circuit(D, K["n_exact"], K["circuit_share"], K["circuit_cap"])
    circ = fc["circuit"]
    diff = (D.acts["clean"] - D.acts["corr"]).mean(0).cpu().numpy()  # (L, F)
    poles = {f: (1 if diff.ravel()[f] >= 0 else -1) for f in fc["order"]}
    log(f"circuit: {len(circ)} neurons, compact={fc['compact']}, curve end {fc['curve'][-1] if fc['curve'] else None}")
    res["circuit"] = {"rule": f"shortest prefix of the exact-effect order removing >= {K['circuit_share']} of the gap (discovery), cap {K['circuit_cap']}",
                      "compact": fc["compact"], "size": len(circ), "curve": fc["curve"],
                      "neurons": [{"id": f, "layer": f // Fd, "neuron": f % Fd, "pole": "+" if poles[f] > 0 else "-",
                                   "exact_effect": fc["exact"][f], "attr_effect": float(fc["attr"].ravel()[f]), "rank": i}
                                  for i, f in enumerate(circ)],
                      "ranked_top": [{"id": f, "layer": f // Fd, "neuron": f % Fd, "pole": "+" if poles[f] > 0 else "-",
                                      "exact_effect": fc["exact"][f]} for f in fc["order"]],
                      "attr_rank_top1000": [int(f) for f in np.argsort(-fc["attr"].ravel())[:1000]],
                      "attr_vs_exact_spearman": float(np.corrcoef(np.argsort(np.argsort([fc["attr"].ravel()[f] for f in fc["top"]])),
                                                                  np.argsort(np.argsort([fc["exact"][f] for f in fc["top"]])))[0, 1])}

    # S3 faithfulness (confirmation split)
    gV = pairs["val"]["g"]
    cmap = C.by_layer(circ, Fd, DEV)
    mgC = V.run("clean", neurons=cmap, src="corr")
    s = {"s1_effect": V.effect(mgC), "s1_ci": ratio_ci(V, mgC, gV)}
    s["s1_holds"] = bool(s["s1_effect"] >= 0.8 and s["s1_ci"][0] >= 0.7)
    rnd = [V.effect(V.run("clean", neurons=C.by_layer(random_matched(circ, Fd, rng, circ), Fd, DEV), src="corr"))
           for _ in range(K["n_random_sets"])]
    s.update({"s2_random_effects_p50_p95": [float(np.percentile(rnd, 50)), float(np.percentile(rnd, 95))]})
    s["s2_holds"] = bool(np.percentile(rnd, 95) <= 0.2)
    mgD = V.run("corr", neurons=cmap, src="clean")
    s.update({"s3_restoration": V.restoration(mgD), "s3_ci": ratio_ci(V, mgD, gV, "restoration")})
    s["s3_holds"] = bool(s["s3_restoration"] >= 0.5)
    log("s1-s3", {k: v for k, v in s.items()})

    mv, sc, ln = data["val"]
    mean_a, _ = T.means(model, *[data["analysis"][i] for i in (0, 2)], DEV)
    bset = T.tactic_sets(mv, ln, max_per_tactic=10 ** 9, seed=SEED)["block"]
    bset_idx_ok = C.block_positions(mv, ln, K["min_stones"])[0]
    keep = np.isin(bset["idx"], bset_idx_ok)
    for k2 in ("idx", "good", "bad", "legal"):
        bset[k2] = bset[k2][keep]
    ctrl = T.control_set(mv, ln, sc, K["control_n"], SEED)
    b0, c0 = T.rate(model, mv, bset, DEV), T.rate(model, mv, ctrl, DEV)
    hk = mean_hook(circ, mean_a, Fd)
    b1, c1 = T.rate(model, mv, bset, DEV, hook=hk), T.rate(model, mv, ctrl, DEV, hook=hk)
    rb = [T.rate(model, mv, bset, DEV, hook=mean_hook(random_matched(circ, Fd, rng, circ), mean_a, Fd)) for _ in range(K["n_random_acc"])]
    s.update({"s4_n_block_positions": int(len(bset["idx"])), "s4_block_acc": [b0, b1], "s4_control_acc": [c0, c1],
              "s4_random_block_drop_median": float(b0 - np.median(rb))})
    s["s4_holds"] = bool((b0 - b1) >= 0.30 and (c0 - c1) <= 0.05 and (b0 - np.median(rb)) <= 0.05)

    hv = res["components"]["val"]["heads"]; mlv = res["components"]["val"]["mlps"]
    top3 = sorted(hv, key=lambda k: -hv[k])[:3]
    s.update({"s5_top3_heads": top3, "s5_top_mlp": max(mlv, key=lambda k: mlv[k])})
    s["s5_holds"] = bool("L0H3" in top3 and s["s5_top_mlp"] == "L5 MLP")

    orient_eff, orient_size = {}, {}
    for i, o in enumerate(C.ORIENT[:3]):
        m = pairs["val"]["orient"] == i
        orient_eff[o] = {"n": int(m.sum()), "effect": V.effect(mgC, m) if m.sum() else None, "ci": None}
        if m.sum():
            mi = np.flatnonzero(m)
            c_, r_ = V.base["clean"][mi], V.base["corr"][mi]
            orient_eff[o]["ci"] = C.boot(lambda ix: (c_[ix].mean() - mgC[mi][ix].mean()) / (c_[ix].mean() - r_[ix].mean()),
                                         gV[mi], K["n_boot"], SEED)
        md = pairs["analysis"]["orient"] == i
        if md.sum() >= 20:
            Po = C.Patcher(model, C.subset(pairs["analysis"], md), DEV, K["bs"])
            fo = C.find_circuit(Po, K["n_exact"], K["circuit_share"], K["circuit_cap"])
            orient_size[o] = {"n_pairs": int(md.sum()), "size": fo["k"], "compact": fo["compact"],
                              "overlap_with_C": len(set(fo["circuit"]) & set(circ))}
            del Po
    s.update({"s6_effect_by_orientation": orient_eff, "s6_circuit_size_by_orientation": orient_size})
    s["s6_holds"] = bool(all(v["effect"] is not None and v["effect"] >= 0.6 for v in orient_eff.values())
                         and len(orient_size) == 3 and min(orient_size, key=lambda o: orient_size[o]["size"]) == "vertical"
                         and sum(v["size"] == orient_size["vertical"]["size"] for v in orient_size.values()) == 1)
    res["faithfulness"] = s
    log("faithfulness", {k: v for k, v in s.items() if k.endswith("holds")})

    # S4 mechanism (descriptive)
    rf, probe_acc = receptive_fields(model, circ, poles, D, Fd)
    PD = pairs["analysis"]
    mech = {"probe_acc_heldout": probe_acc, "neurons": {}}
    for f in circ:
        dla = direct_logit(model, f, Fd)
        dl = fc["deltas"][f]
        by_col = {}
        for c in range(7):
            m = PD["block_col"] == c
            if m.sum() >= 10:
                by_col[c] = float(dl[m].mean() / (D.base["clean"][m].mean() - D.base["corr"][m].mean()))
        by_or = {}
        for i, o in enumerate(C.ORIENT):
            m = PD["orient"] == i
            if m.sum() >= 10:
                by_or[o] = float(dl[m].mean() / (D.base["clean"][m].mean() - D.base["corr"][m].mean()))
        promotes = int(np.argmax(np.array(dla) * poles[f]))
        mech["neurons"][str(f)] = {"receptive_field": rf[f], "direct_logit_centred": dla, "promotes_col": promotes,
                                   "effect_by_block_col": by_col, "effect_by_orientation": by_or,
                                   "best_block_col": max(by_col, key=lambda c: by_col[c]) if by_col else None}
    al = [v["promotes_col"] == v["best_block_col"] for v in mech["neurons"].values() if v["best_block_col"] is not None]
    mech["share_promoting_own_block_col"] = float(np.mean(al)) if al else None
    res["mechanism"] = mech
    res["examples"] = [{"clean": PD["clean"][i][:PD["t"][i]].tolist(), "corr": PD["corr"][i][:PD["t"][i]].tolist(),
                        "block_col": int(PD["block_col"][i]), "orient": C.ORIENT[PD["orient"][i]]} for i in range(min(40, len(PD["t"])))]
    res["seconds"] = round(time.time() - t0, 1)
    OUT.write_text(json.dumps(res, indent=1))
    provenance.write(OUT, K)
    log(f"wrote {OUT} in {res['seconds']}s")


if __name__ == "__main__":
    main()
