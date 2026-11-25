"""PLAN.md addendum (v), V1-V5: what neurons write. Column readouts through the J-lens and the logit lens, a concept lens onto the
exact concepts, an output-side polysemanticity taxonomy, the fixed-basis test and readable removal for vertical blocks.
Writes results/outputs_v15.json (all measures and predictions) and results/outputs_readouts.npz (per-pole readouts, used by
scripts 49 and 50). SMOKE=1: wiring check, numbers meaningless. Run on a GPU host."""
import json
import os
import re
import time

import numpy as np
import torch
from scipy.optimize import nnls

from c4n import circuit as C
from c4n import config, ns, provenance
from c4n import outputs as O
from c4n import worldmodel as WM
from c4n.concepts import NAMES
from c4n.data import concepts_for
from c4n.model import tokens_from_moves
from c4n.tactics import margin, position_index

CFG = config.load("outputs")
SMOKE = bool(os.environ.get("SMOKE"))
K = {**CFG, **(CFG["smoke"] if SMOKE else {})}
DEV = "cuda" if torch.cuda.is_available() else "cpu"
ROOT = config.ROOT
RES = config.results_dir(CFG)
TAG = "_smoke" if SMOKE else ""
OUT = RES / f"outputs_v15{TAG}.json"
NPZ = RES / f"outputs_readouts{TAG}.npz"
rng = np.random.default_rng(K["seed"])


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def col_concepts(c):
    """Concept indices about column c (V5 readable set)."""
    pat = re.compile(rf"^(block_now_c{c}|win_now_c{c}|full_c{c}|last_col_c{c}|land_r\dc{c}|cell_r\dc{c}_\w+|(my|opp)_threat_r\dc{c}"
                     rf"|line_v_r\dc{c}_\w+)$")
    return [i for i, n in enumerate(NAMES) if pat.match(n)]


def main():
    t0 = time.time()
    model = ns.load_web_model(DEV)
    L, Fd, d = model.cfg["n_layer"], model.cfg["d_ff"], model.cfg["d_model"]
    n = K["n_games"]
    dmv, dsc, dln = ns.load_games("analysis", n)
    tmv, tsc, tln = ns.load_games("val", n)
    dg, dt = position_index(dln)
    tg, tt = position_index(tln)
    delig, telig = dt >= K["min_ply"], tt >= K["min_ply"]
    log("collect")
    Dd = O.collect(model, dmv, dln, DEV)
    Dt = O.collect(model, tmv, tln, DEV)
    log("concept labels")
    Yd = concepts_for({"data": CFG["data"]}, "analysis", n)
    Yt = concepts_for({"data": CFG["data"]}, "val", n)
    assert len(Yd) == len(dg) and len(Yt) == len(tg)

    # ---------------------------------------------------------- poles: thresholds, use
    q = K["fire_pct"]
    from c4n.analysis import percentiles
    P = percentiles(Dd["a"][torch.as_tensor(delig)], [1, 100 - q, q, 99], DEV)  # (4, L, F)
    thr_pos, thr_neg, p99_pos, p1 = P[2], P[1], P[3], P[0]
    ea = Dd["a"][torch.as_tensor(delig)]
    dev_mean = ea.float().mean(0)
    dev_std = ea.float().std(0) + 1e-6
    used = np.zeros(2 * L * Fd, bool)
    n_fire = np.zeros(2 * L * Fd, int)
    for l in range(L):
        fr = O.firing(ea, Dd["gate"][torch.as_tensor(delig)], thr_pos, thr_neg, l).sum(0).numpy()  # (F, 2)
        n_fire[2 * l * Fd:2 * (l + 1) * Fd] = fr.reshape(-1)
    used = n_fire >= K["min_firings"]
    size = np.zeros(2 * L * Fd)  # p99 of s.a (natural strong activation)
    size[0::2] = p99_pos.reshape(-1).clamp_min(0).numpy(); size[1::2] = (-p1).reshape(-1).clamp_min(0).numpy()
    log(f"used poles {used.sum()} of {len(used)}")

    # ---------------------------------------------------------- lenses
    log("jacobians")
    jsel = np.sort(rng.choice(np.flatnonzero(delig), min(K["jac_positions"], delig.sum()), replace=False))
    J, Rres = O.jacobians(model, dmv, dln, jsel, DEV, bs=500)
    Wout = O.out_vectors(model)  # (L, F, d)
    S = torch.tensor([1.0, -1.0])
    V = (Wout[:, :, None, :] * S[None, None, :, None]).reshape(L * Fd * 2, d)  # pole vectors s w, pid order
    lay = np.repeat(np.arange(L), Fd * 2)
    readJ = torch.einsum("pkd,pd->pk", J[lay], V).numpy()          # (P, 7)
    readD = (V @ J[L - 1].T).numpy()                                  # logit lens = the last-layer Jacobian
    topJ, topD = readJ.argmax(1), readD.argmax(1)

    log("probes")
    psel = np.sort(rng.choice(np.flatnonzero(delig), min(K["probe_positions"], delig.sum()), replace=False))
    Xf_d = Dd["resid"][:, -1].float()
    Wp, bp = O.fit_probes(Xf_d[psel], Yd[psel], DEV, steps=K["probe_steps"])
    zd = Xf_d[torch.as_tensor(delig)] @ Wp + bp
    zsd = zd.std(0) + 1e-6
    zt = (Dt["resid"][:, -1].float() @ Wp + bp)
    au = O.auroc_cols(zt[torch.as_tensor(telig)], Yt[telig], DEV).numpy()
    rate = Yd[delig].mean(0)
    readable = (au >= K["readable_auroc"]) & (rate >= K["readable_rate"][0]) & (rate <= K["readable_rate"][1])
    log(f"readable concepts {readable.sum()} of {len(NAMES)}")
    Kl = torch.einsum("dk,lde->lke", Wp, Rres) / zsd[None, :, None]   # (L, K, d)
    readC = torch.einsum("pkd,pd->pk", Kl[lay], V).numpy()           # (P, K)
    PHI = O.phi(Yd[delig], DEV).numpy()

    # ---------------------------------------------------------- J-share
    log("J-share")
    jshare = np.full(len(V), np.nan)
    rand_q = {}
    for l in range(L):
        A = J[l].T.numpy().astype(np.float64)
        for p in np.flatnonzero(used & (lay == l)):
            v = V[p].numpy().astype(np.float64)
            _, r = nnls(A, v)
            jshare[p] = 1 - r ** 2 / (v @ v)
        R = np.random.default_rng(K["seed"] + l).standard_normal((K["n_random_dirs"], d))
        rs = np.array([1 - nnls(A, x)[1] ** 2 / (x @ x) for x in R])
        rand_q[l] = (float(np.percentile(rs, 1)), float(np.percentile(rs, 99)))

    # ---------------------------------------------------------- causal effects of zeroing each used pole on its test firing set
    log("causal zeroing")
    tea = Dt["a"]
    rows_p, rows_i = [], []
    for l in range(L):
        fr = O.firing(tea, Dt["gate"], thr_pos, thr_neg, l) & torch.as_tensor(telig)[:, None, None]
        for j in range(2):
            nz = torch.nonzero(fr[:, :, j])  # (k, 2): position, neuron
            if len(nz) == 0:
                continue
            nz = nz.numpy()
            order = np.lexsort((rng.random(len(nz)), nz[:, 1]))
            nz = nz[order]
            starts = np.searchsorted(nz[:, 1], np.arange(Fd)); ends = np.searchsorted(nz[:, 1], np.arange(Fd), "right")
            for nn_ in range(Fd):
                p = (l * Fd + nn_) * 2 + j
                if not used[p] or ends[nn_] == starts[nn_]:
                    continue
                pos = nz[starts[nn_]:min(ends[nn_], starts[nn_] + K["max_fire_rows"]), 0]
                rows_p.append(np.full(len(pos), p)); rows_i.append(pos)
    rows_p, rows_i = np.concatenate(rows_p), np.concatenate(rows_i)
    log(f"rows {len(rows_p):,}")
    nP = len(V)
    dcol = torch.zeros(nP, 7, device=DEV); dcon = torch.zeros(nP, len(NAMES), device=DEV); cnt = torch.zeros(nP, device=DEV)
    Wp_d, bp_d, zsd_d = Wp.to(DEV), bp.to(DEV), zsd.to(DEV)
    bs = K["bs"]
    with torch.no_grad():
        for s in range(0, len(rows_p), bs):
            pp, ii = rows_p[s:s + bs], rows_i[s:s + bs]
            tok = tokens_from_moves(torch.as_tensor(tmv[tg[ii]])).to(DEV)
            tq = torch.as_tensor(tt[ii], device=DEV); ar = torch.arange(len(ii), device=DEV)
            l_ = torch.as_tensor(pp // 2 // Fd, device=DEV); n_ = torch.as_tensor(pp // 2 % Fd, device=DEV)
            s_ = torch.as_tensor(np.where(pp % 2 == 0, 1.0, -1.0), device=DEV)
            lg0, k0 = WM.run(model, tok, keep={2 * L})
            lg1, k1 = WM.run(model, tok, mlp_hook=O.PoleZero(l_, n_, s_), keep={2 * L})
            dc = O.centered(lg0[ar, tq]) - O.centered(lg1[ar, tq])
            dz = ((k0[2 * L][ar, tq] - k1[2 * L][ar, tq]) @ Wp_d) / zsd_d
            pt = torch.as_tensor(pp, device=DEV)
            dcol.index_add_(0, pt, dc); dcon.index_add_(0, pt, dz); cnt.index_add_(0, pt, torch.ones(len(pp), device=DEV))
    has = (cnt > 0).cpu().numpy()
    dcol = (dcol / cnt.clamp_min(1)[:, None]).cpu().numpy(); dcon = (dcon / cnt.clamp_min(1)[:, None]).cpu().numpy()

    # ---------------------------------------------------------- V1
    causal_col = dcol.argmax(1)
    meas1 = used & has & (dcol.max(1) >= K["col_measurable"])
    v1 = {"per_layer": {}}
    for l in range(L):
        m = meas1 & (lay == l)
        v1["per_layer"][l] = {"measurable": int(m.sum()), "used": int((used & (lay == l)).sum()),
                              "agree_J": float((topJ[m] == causal_col[m]).mean()) if m.any() else None,
                              "agree_logit": float((topD[m] == causal_col[m]).mean()) if m.any() else None,
                              "jshare_high": float((jshare[used & (lay == l)] > rand_q[l][1]).mean()),
                              "jshare_low": float((jshare[used & (lay == l)] < rand_q[l][0]).mean()),
                              "jshare_median": float(np.nanmedian(jshare[used & (lay == l)])), "random_q01_q99": rand_q[l]}
    m04, m03 = meas1 & (lay <= 4), meas1 & (lay <= 3)
    aJ04 = float((topJ[m04] == causal_col[m04]).mean())
    aJ03, aD03 = float((topJ[m03] == causal_col[m03]).mean()), float((topD[m03] == causal_col[m03]).mean())
    m5 = meas1 & (lay == 5)
    aJ5, aD5 = float((topJ[m5] == causal_col[m5]).mean()), float((topD[m5] == causal_col[m5]).mean())
    v1["v_1"] = {"agree_J_layers0_4": aJ04, "agree_J_layers0_3": aJ03, "agree_logit_layers0_3": aD03,
                 "holds": bool(aJ04 >= 0.5 and aJ03 - aD03 >= 0.15)}
    v1["v_2"] = {"agree_J_layer5": aJ5, "agree_logit_layer5": aD5, "holds": bool(aJ5 >= 0.8 and aD5 >= 0.8),
                 "note": "in layer 5 the two lenses are the same Jacobian by construction"}
    hi = {l: v1["per_layer"][l]["jshare_high"] for l in range(L)}
    v1["v_3"] = {"high_share": hi, "holds": bool(hi[5] >= 0.20 and all(hi[l] >= 0.05 for l in range(5)))}

    # ---------------------------------------------------------- V2
    rd = np.flatnonzero(readable)
    cc = dcon[:, rd]; rc = readC[:, rd]
    meas2 = used & has & (cc.max(1) >= K["concept_measurable"])
    top5 = np.argsort(-cc, 1)[:, :5]
    rtop = rc.argmax(1)
    hit = np.array([rtop[p] in top5[p] for p in range(nP)])
    base_hit = np.zeros(nP, bool)
    for l in range(L):
        pool = np.flatnonzero(used & (lay == l))
        for p in np.flatnonzero(meas2 & (lay == l)):
            o = rng.choice(pool[pool != p]) if len(pool) > 1 else p
            base_hit[p] = rtop[o] in top5[p]
    m = meas2 & (lay <= 4)
    v2 = {"readable_concepts": int(readable.sum()), "measurable_layers0_4": int(m.sum()),
          "per_layer": {l: {"measurable": int((meas2 & (lay == l)).sum()),
                            "top1_in_causal_top5": float(hit[meas2 & (lay == l)].mean()) if (meas2 & (lay == l)).any() else None,
                            "baseline": float(base_hit[meas2 & (lay == l)].mean()) if (meas2 & (lay == l)).any() else None}
                        for l in range(L)}}
    h, b = float(hit[m].mean()), float(base_hit[m].mean())
    v2["v_4"] = {"top1_in_causal_top5": h, "baseline": b, "ratio": h / b if b > 0 else None, "holds": bool(h >= 0.5 and h >= 5 * b)}
    # input side (what it fires on) vs output side (what it adds)
    pt = json.loads((RES / "pole_table.json").read_text())
    in_c = np.full(nP, -1); in_f1 = np.full(nP, np.nan)
    idx = {k: i for i, k in enumerate(NAMES)}
    for r in pt:
        p = O.pid(r["layer"], r["neuron"], 1 if r["pole"] == "+" else -1, Fd)
        in_c[p] = idx.get(r["concept_p97"], -1); in_f1[p] = r["f1_p97"]
    out_c = rd[cc.argmax(1)]
    ok = meas2 & (in_c >= 0)
    same = ok & (in_c == out_c)
    rel = ok & (np.abs(np.nan_to_num(PHI[np.clip(in_c, 0, None), out_c])) >= K["related_phi"])
    v2["input_vs_output"] = {"n": int(ok.sum()), "same_concept": float(same.sum() / max(1, ok.sum())),
                             "same_or_related": float((same | rel).sum() / max(1, ok.sum()))}

    # ---------------------------------------------------------- V3
    absphi = np.abs(np.nan_to_num(PHI[np.ix_(rd, rd)]))
    t3 = np.zeros(nP, bool); adds = {}
    for p in np.flatnonzero(meas2):
        mx = cc[p].max()
        a_ = np.flatnonzero((cc[p] >= K["concept_measurable"]) & (cc[p] >= K["adds_frac"] * mx))
        adds[p] = a_
        if len(a_) > 1:
            sub = absphi[np.ix_(a_, a_)]
            t3[p] = bool((sub[np.triu_indices(len(a_), 1)] < K["unrelated_phi"]).any())
    t2 = []
    for nn_ in range(L * Fd):
        p0, p1_ = 2 * nn_, 2 * nn_ + 1
        if meas2[p0] and meas2[p1_] and absphi[cc[p0].argmax(), cc[p1_].argmax()] < K["unrelated_phi"]:
            t2.append(nn_)
    t1 = meas2 & ~t3 & (np.nan_to_num(in_f1, nan=1.0) < 0.3)

    def ex(p):
        l, nn_, s = O.unpid(int(p), Fd)
        return {"layer": int(l), "neuron": int(nn_), "pole": "+" if s > 0 else "-",
                "adds": [NAMES[rd[i]] for i in adds.get(p, cc[p].argsort()[::-1][:3])][:4],
                "fires_on": NAMES[in_c[p]] if in_c[p] >= 0 else None, "fires_on_f1": float(in_f1[p])}
    v3 = {"measurable": int(meas2.sum()), "type3": int(t3.sum()), "type3_share": float(t3.sum() / max(1, meas2.sum())),
          "type2_neurons": len(t2), "type1": int(t1.sum()), "type1_share": float(t1.sum() / max(1, meas2.sum())),
          "examples": {"type3": [ex(p) for p in np.flatnonzero(t3)[:8]],
                       "type2": [[ex(2 * nn_), ex(2 * nn_ + 1)] for nn_ in t2[:6]],
                       "type1": [ex(p) for p in np.flatnonzero(t1)[np.argsort(-cc[t1].max(1))][:8]]}}
    v3["v_5"] = {"type3_share": v3["type3_share"], "holds": bool(v3["type3_share"] <= 0.05)}

    # ---------------------------------------------------------- V4 fixed basis
    log("fixed basis")
    vm = json.loads((RES / "vertical_map.json").read_text())
    Rp = [O.pid(5, x["neuron"], 1 if x["pole"] == "+" else -1, Fd) for x in vm["circuit"]["neurons"] if x["layer"] == 5]
    gainJ = readJ[np.arange(nP), topJ] * size
    vecs = [(p, "R") for p in Rp]
    for l in range(5):
        cand = np.flatnonzero(used & (lay == l))
        for p in cand[np.argsort(-gainJ[cand])][:K["fb_per_layer"]]:
            g_d = readD[p, topJ[p]]
            vecs.append((int(p), "direct" if topD[p] == topJ[p] and g_d >= 0.5 * readJ[p, topJ[p]] else "indirect"))
    fsel = np.sort(rng.choice(np.flatnonzero(telig), min(K["fb_positions"], telig.sum()), replace=False))
    tok_f = tokens_from_moves(torch.as_tensor(tmv[tg[fsel]])).to(DEV)
    tq_f = torch.as_tensor(tt[fsel], device=DEV)
    base_f = Dt["logits"][fsel].to(DEV)
    nr = K["fb_random"]
    gens = {lp: torch.as_tensor(np.random.default_rng(K["seed"] + 100 + lp).standard_normal((nr, d)), dtype=torch.float32,
                                device=DEV) for lp in range(L)}
    fb_rows = []
    chunk = max(1, 8192 // len(fsel))
    with torch.no_grad():
        for p, kind in vecs:
            v = (V[p] * float(size[p])).to(DEV)
            c = int(topJ[p])
            for lp in range(L):
                rnd = gens[lp] / gens[lp].norm(dim=1, keepdim=True) * v.norm()
                allv = torch.cat([v[None], rnd])  # (1 + nr, d)
                gains = []
                for s in range(0, len(allv), chunk):
                    vv = allv[s:s + chunk]; m_ = len(vv)
                    tok = tok_f.repeat(m_, 1); tq = tq_f.repeat(m_); ar = torch.arange(len(tok), device=DEV)
                    add = vv.repeat_interleave(len(fsel), 0)

                    def rh(pt_, x, lp=lp, ar=ar, tq=tq, add=add):
                        if pt_ == 2 * lp + 2:
                            x = x.clone(); x[ar, tq] = x[ar, tq] + add
                        return x
                    lg, _ = WM.run(model, tok, resid_hook=rh)
                    dl = O.centered(lg[ar, tq])[:, c] - base_f[:, c].repeat(m_)
                    gains += dl.view(m_, len(fsel)).mean(1).tolist()
                fb_rows.append({"pid": int(p), "layer": int(lay[p]), "kind": kind, "inject_layer": lp, "gain": gains[0],
                                "random_p95": float(np.percentile(gains[1:], 95)), "beats": bool(gains[0] > np.percentile(gains[1:], 95))})
    v4 = {"rows": fb_rows}
    for kind in ("R", "direct", "indirect"):
        rr = [r for r in fb_rows if r["kind"] == kind and r["inject_layer"] <= 4]
        v4[f"beats_share_{kind}"] = float(np.mean([r["beats"] for r in rr])) if rr else None
        v4[f"n_{kind}"] = len({r["pid"] for r in fb_rows if r["kind"] == kind})
    v4["v_6"] = {"holds": bool(all((v4[f"beats_share_{k}"] or 0) >= 0.8 for k in ("direct", "indirect") if v4[f"n_{k}"]))}

    # ---------------------------------------------------------- V5 readable removal (vertical must-block)
    log("readable removal")
    idx_b, B = C.block_positions(tmv, tln, K["min_ply"])
    opp, cell = (B["pos"] ^ B["mask"])[idx_b], B["op_w"][idx_b]
    kinds = np.stack([np.any([(C.winning_dir(opp, B["mask"][idx_b], dd) & cell) != 0 for dd in ds], 0) for ds in C.DIRS.values()], 1)
    vert = idx_b[kinds[:, 0] & ~kinds[:, 1] & ~kinds[:, 2]]
    vsel = np.sort(rng.choice(vert, min(K["rm_positions"], len(vert)), replace=False))
    bcol = B["block"][vsel].argmax(1)
    legal = B["legal"][vsel]
    u5 = np.flatnonzero(used & (lay == 5))
    writers_all = u5[np.argsort(-gainJ[u5])][:max(1, int(round(K["writer_frac"] * len(u5))))]
    Wc = {c: [int(p) for p in writers_all if topJ[p] == c] for c in range(7)}
    readset = {}
    for c in range(7):
        cs = set(col_concepts(c))
        top5c = np.argsort(-readC, 1)[:, :5]
        m_ = used & ((topJ == c) | np.array([bool(cs.intersection(top5c[p])) for p in range(nP)]))
        readset[c] = np.setdiff1d(np.flatnonzero(m_), Wc[c])
    mean_d = dev_mean.to(DEV)
    # attribution of each pole to the block margin (gradient x (mean - activation), active positions only)
    attr = np.zeros((len(vsel), nP), np.float32)
    tq_all = tt[vsel]
    for s in range(0, len(vsel), 250):
        sl = slice(s, s + 250)
        tok = tokens_from_moves(torch.as_tensor(tmv[tg[vsel[sl]]])).to(DEV)
        tq = torch.as_tensor(tq_all[sl], device=DEV); ar = torch.arange(len(tq), device=DEV)
        store = {}

        def mh(l, a, g, u):
            a.retain_grad(); store[l] = (a, g); return a
        with torch.enable_grad():
            lg, _ = WM.run(model, tok, mlp_hook=mh)
            good = torch.nn.functional.one_hot(torch.as_tensor(bcol[sl], device=DEV), 7).bool()
            margin(lg[ar, tq], good, torch.as_tensor(legal[sl], device=DEV)).sum().backward()
        for l in range(L):
            a, g = store[l]
            gx = a.grad * (mean_d[l][None, None] - a.detach())
            op = g.detach() > 0
            ap = (gx * ((a.detach() > 0) & op)).sum(1); an = (gx * ((a.detach() < 0) & op)).sum(1)
            attr[sl, 2 * l * Fd:2 * (l + 1) * Fd] = torch.stack([ap, an], -1).reshape(len(tq), -1).cpu().numpy()
        model.zero_grad(set_to_none=True)
    orders = [readset[c][np.argsort(attr[i, readset[c]])] for i, c in enumerate(bcol)]

    def masks(sets):
        mp = torch.zeros(len(sets), L, Fd, dtype=torch.bool, device=DEV); mn = torch.zeros_like(mp)
        for i, ps in enumerate(sets):
            ps = np.asarray(ps, int)
            if len(ps) == 0:
                continue
            l_, n_, j_ = ps // 2 // Fd, ps // 2 % Fd, ps % 2
            mp[i, l_[j_ == 0], n_[j_ == 0]] = True; mn[i, l_[j_ == 1], n_[j_ == 1]] = True
        return mp, mn

    @torch.no_grad()
    def picks(sets):
        out = []
        for s in range(0, len(vsel), 250):
            sl = slice(s, s + 250)
            tok = tokens_from_moves(torch.as_tensor(tmv[tg[vsel[sl]]])).to(DEV)
            tq = torch.as_tensor(tq_all[sl], device=DEV); ar = torch.arange(len(tq), device=DEV)
            mp, mn = masks(sets[sl])
            lg, _ = WM.run(model, tok, mlp_hook=O.PoleMean(mp, mn, mean_d))
            out.append(lg[ar, tq].masked_fill(~torch.as_tensor(legal[sl], device=DEV), -1e9).argmax(-1).cpu().numpy())
        return np.concatenate(out)
    base_pick = picks(np.array([[] for _ in vsel], dtype=object))
    w_pick = picks(np.array([Wc[c] for c in bcol], dtype=object))
    flip_k = np.full(len(vsel), -1); flip_move = np.full(len(vsel), -1)
    for k in range(0, K["rm_cap"] + 1, K["rm_step"]):
        sets = np.empty(len(vsel), dtype=object)
        for i, c in enumerate(bcol):
            sets[i] = list(Wc[c]) + list(orders[i][:k])
        pk = picks(sets)
        new = (flip_k < 0) & (pk != bcol)
        flip_k[new] = k; flip_move[new] = pk[new]
        if (flip_k >= 0).all():
            break
    fl = flip_k >= 0
    rnd_sets = np.empty(len(vsel), dtype=object)
    for i, c in enumerate(bcol):
        pool = np.setdiff1d(np.flatnonzero(used), np.concatenate([readset[c], Wc[c]]).astype(int))
        nn_ = len(Wc[c]) + max(0, flip_k[i])
        rnd_sets[i] = list(rng.choice(pool, nn_, replace=False)) if fl[i] else []
    r_pick = picks(rnd_sets)
    sc = tsc[tg[vsel], tq_all].astype(float)
    best_nb = np.where(legal & (np.arange(7)[None] != bcol[:, None]), sc, -1e9).argmax(1)
    v5 = {"n_positions": int(len(vsel)), "n_vertical": int(len(vert)), "base_block_rate": float((base_pick == bcol).mean()),
          "writers_per_col": {c: len(Wc[c]) for c in range(7)}, "readable_per_col": {c: int(len(readset[c])) for c in range(7)},
          "writers_in_R": int(len(set(writers_all.tolist()) & set(Rp))), "n_writers": int(len(writers_all)),
          "block_kept_after_writers": float((w_pick == bcol).mean()),
          "flipped_within_cap": float(fl.mean()), "median_extra_poles_to_flip": float(np.median(flip_k[fl])) if fl.any() else None,
          "random_flip_rate_at_flip_counts": float((r_pick[fl] != bcol[fl]).mean()) if fl.any() else None,
          "after_flip_is_teacher_best_nonblock": float((flip_move[fl] == best_nb[fl]).mean()) if fl.any() else None}
    v5["v_7"] = {"holds": bool(v5["block_kept_after_writers"] >= 0.5)}
    rf = v5["random_flip_rate_at_flip_counts"]
    v5["v_8"] = {"holds": bool(fl.mean() >= 0.9 and rf is not None and rf <= 0.10)}

    out = {"study": "(v) V1-V5, PLAN.md addendum (v)", "smoke": SMOKE, "n_used_poles": int(used.sum()), "V1": v1, "V2": v2, "V3": v3,
           "V4": v4, "V5": v5, "seconds": round(time.time() - t0, 1)}
    OUT.write_text(json.dumps(out, indent=1, default=float))
    np.savez_compressed(NPZ, used=used, n_fire=n_fire, size=size, readJ=readJ, readD=readD, topJ=topJ, jshare=jshare,
                        readC=readC.astype(np.float16), dcol=dcol, dcon=dcon.astype(np.float16), readable=readable, probe_auroc=au,
                        thr_pos=thr_pos.numpy(), thr_neg=thr_neg.numpy(), dev_mean=dev_mean.numpy(), dev_std=dev_std.numpy(),
                        J=J.numpy(), Rres=Rres.numpy(), Wp=Wp.numpy(), bp=bp.numpy(), zsd=zsd.numpy())
    provenance.write(OUT, K)
    log("done", json.dumps({k: out[k][kk] for k in ("V1", "V2", "V3", "V4", "V5") for kk in out[k] if kk.startswith("v_")}, default=float)[:2000])


if __name__ == "__main__":
    main()
