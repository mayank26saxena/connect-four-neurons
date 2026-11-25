"""PLAN.md addendum (v), V6-V7: neurons as zero-label probes and as steering vectors, for "the opponent threatens column c".
Needs results/outputs_readouts.npz from scripts/48_readouts.py. Writes results/outputs_v67.json. SMOKE=1: wiring check. GPU host."""
import itertools
import json
import os
import time

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from c4n import config, ns, provenance
from c4n import engine as E
from c4n import outputs as O
from c4n import worldmodel as WM
from c4n.concepts import NAMES
from c4n.data import concepts_for
from c4n.model import tokens_from_moves
from c4n.tactics import COLMASK, position_index

CFG = config.load("outputs")
SMOKE = bool(os.environ.get("SMOKE"))
K = {**CFG, **(CFG["smoke"] if SMOKE else {})}
DEV = "cuda" if torch.cuda.is_available() else "cpu"
RES = config.results_dir(CFG)
TAG = "_smoke" if SMOKE else ""
OUT = RES / f"outputs_v67{TAG}.json"
IDX = {k: i for i, k in enumerate(NAMES)}


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def examples(c, n):
    """Sequences written by rule: the second player stacks three in column c; the first player plays filler columns; the result
    must have exactly one threat (column c) for the player to move and no win for them. n spread over the valid list."""
    ok = []
    for f in itertools.product([x for x in range(7) if x != c], repeat=3):
        seq = [f[0], c, f[1], c, f[2], c]
        p, m = E.replay_boards(np.array(seq, np.int8))
        P, M = p[6:7], m[6:7]
        play = E.playable(M)
        if (E.winning_cells(P, M) & play)[0] != 0:
            continue
        if (E.winning_cells(P ^ M, M) & play)[0] != (play & COLMASK[c])[0]:
            continue
        ok.append(seq)
    pick = np.linspace(0, len(ok) - 1, n).round().astype(int)
    return [ok[i] for i in pick]


def main():
    t0 = time.time()
    rng = np.random.default_rng(K["seed"] + 6)
    R = np.load(RES / f"outputs_readouts{TAG}.npz")
    used, topJ, size = R["used"], R["topJ"], R["size"]
    model = ns.load_web_model(DEV)
    L, Fd, d = model.cfg["n_layer"], model.cfg["d_ff"], model.cfg["d_model"]
    Wout = O.out_vectors(model)
    n = K["n_games"]
    dmv, dsc, dln = ns.load_games("analysis", n)
    tmv, tsc, tln = ns.load_games("val", n)
    dg, dt = position_index(dln); tg, tt = position_index(tln)
    delig, telig = dt >= K["min_ply"], tt >= K["min_ply"]
    Dd = O.collect(model, dmv, dln, DEV); Dt = O.collect(model, tmv, tln, DEV)
    Yd = concepts_for({"data": CFG["data"]}, "analysis", n); Yt = concepts_for({"data": CFG["data"]}, "val", n)
    mean, std = torch.as_tensor(R["dev_mean"]), torch.as_tensor(R["dev_std"])
    pts = Dd["points"]

    def vec(p):
        l, nn_, s = O.unpid(int(p), Fd)
        return l, s * Wout[l, nn_]

    # ---------------------------------------------------------- V6 zero-label probes
    chosen, v6 = {}, {"columns": {}}
    for c in range(7):
        ex = examples(c, K["zl_examples"])
        tok = tokens_from_moves(torch.as_tensor(np.array(ex, np.int8))).to(DEV)
        store = {}
        with torch.no_grad():
            model(tok, hook=lambda l, a, g, u: (store.__setitem__(l, a[:, 6].cpu()), a)[1])
        acts = torch.stack([store[l] for l in range(L)], 1)  # (n_ex, L, F)
        z = ((acts - mean) / std).mean(0).reshape(-1)       # (L*F)
        zp = torch.stack([z, -z], -1).reshape(-1).numpy()    # pid order
        cand = np.flatnonzero(used & (topJ == c))
        chosen[c] = cand[np.argsort(-zp[cand])][:K["zl_poles"]]
        y = Yt[telig, IDX[f"block_now_c{c}"]]
        score = np.zeros(int(telig.sum()))
        for p in chosen[c]:
            l, v = vec(p)
            X = Dt["resid"][torch.as_tensor(telig), pts.index(2 * l + 2)].float()
            score += torch.nn.functional.cosine_similarity(X, v[None], dim=1).numpy()
        zl = float(roc_auc_score(y, score))
        heur = float(roc_auc_score(y, Yt[telig, IDX[f"last_col_c{c}"]].astype(float)))
        yd = Yd[delig, IDX[f"block_now_c{c}"]]
        probes = {}
        for nl in K["zl_labels"]:
            aus = []
            for sd in range(K["zl_seeds"]):
                r = np.random.default_rng(K["seed"] + 1000 * nl + sd)
                pos_i, neg_i = np.flatnonzero(yd), np.flatnonzero(~yd)
                sel = np.concatenate([r.choice(pos_i, nl // 2, replace=False), r.choice(neg_i, nl // 2, replace=False)])
                ys = yd[sel]
                best, bl = -1, None
                for pt_ in (8, 10, 12):
                    Xs = Dd["resid"][torch.as_tensor(np.flatnonzero(delig)[sel]), pts.index(pt_)].float().numpy()
                    cv = []
                    for tr, te in StratifiedKFold(5, shuffle=True, random_state=sd).split(Xs, ys):
                        m_ = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(Xs[tr], ys[tr])
                        cv.append(roc_auc_score(ys[te], m_.decision_function(Xs[te])))
                    if np.mean(cv) > best:
                        best, bl = float(np.mean(cv)), pt_
                Xs = Dd["resid"][torch.as_tensor(np.flatnonzero(delig)[sel]), pts.index(bl)].float().numpy()
                m_ = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(Xs, ys)
                Xt = Dt["resid"][torch.as_tensor(telig), pts.index(bl)].float().numpy()
                aus.append(float(roc_auc_score(y, m_.decision_function(Xt))))
            probes[nl] = float(np.mean(aus))
        v6["columns"][c] = {"zero_label": zl, "heuristic_last_col": heur, **{f"probe_{k}": v for k, v in probes.items()},
                            "chosen": [dict(zip(("layer", "neuron", "sign"), map(int, O.unpid(int(p), Fd)))) for p in chosen[c]],
                            "examples": ex}
        n1, n2 = K["zl_labels"]
        log(f"V6 col {c}: zero-label {zl:.3f}, {n1} labels {probes[n1]:.3f}, {n2} labels {probes[n2]:.3f}, heuristic {heur:.3f}")
    cols = v6["columns"].values()
    n1, n2 = K["zl_labels"]
    n_ge40 = sum(x["zero_label"] >= x[f"probe_{n1}"] for x in cols)
    n_ge400 = sum(x["zero_label"] >= x[f"probe_{n2}"] - 0.02 for x in cols)
    n_heur = sum(x["zero_label"] > x["heuristic_last_col"] for x in cols)
    v6["v_9"] = {"cols_ge_40_label_probe": n_ge40, "cols_within_0.02_of_400": n_ge400, "cols_above_heuristic": n_heur,
                 "holds": bool(n_ge40 >= 4 and n_heur == 7)}

    # ---------------------------------------------------------- V7 steering
    win_any, blk_any = IDX["win_now_any"], IDX["block_now_any"]

    def control(mv, sc, g, t, elig, Y, c, cap, seed):
        lg_ = sc[g, t] != E.ILLEGAL
        others = lg_.sum(1) - lg_[:, c]
        m_ = elig & ~Y[:, win_any] & ~Y[:, blk_any] & lg_[:, c] & (others >= 2)
        i = np.flatnonzero(m_)
        return np.sort(np.random.default_rng(seed).choice(i, min(cap, len(i)), replace=False))

    @torch.no_grad()
    def rate(mv, sc, g, t, sel, c, adds):
        """Share of positions where the greedy legal move is c, with `adds` {point: vector} added at every position."""
        hits = 0
        for s in range(0, len(sel), 1000):
            ii = sel[s:s + 1000]
            tok = tokens_from_moves(torch.as_tensor(mv[g[ii]])).to(DEV)
            tq = torch.as_tensor(t[ii], device=DEV); ar = torch.arange(len(ii), device=DEV)

            def rh(p, x):
                return x + adds[p].to(DEV) if p in adds else x
            lg, _ = WM.run(model, tok, resid_hook=rh if adds else None)
            legal = torch.as_tensor(sc[g[ii], t[ii]] != E.ILLEGAL, device=DEV)
            hits += int((lg[ar, tq].masked_fill(~legal, -1e9).argmax(-1) == c).sum())
        return hits / max(1, len(sel))

    def pole_adds(ps, total=None):
        adds, tot = {}, 0.0
        for p in ps:
            l, v = vec(p)
            adds[2 * l + 2] = adds.get(2 * l + 2, 0) + float(size[p]) * v
            tot += float(size[p]) * float(v.norm())
        if total is not None:
            adds = {k: x * (total / tot) for k, x in adds.items()}
        return adds, tot

    v7 = {"columns": {}}
    for c in range(7):
        dsel = control(dmv, dsc, dg, dt, delig, Yd, c, K["st_dev_positions"], K["seed"] + c)
        tsel = control(tmv, tsc, tg, tt, telig, Yt, c, K["st_test_positions"], K["seed"] + 50 + c)
        base_adds, tot1 = pole_adds(chosen[c])
        beta = K["st_betas"][-1]
        dev_rates = {}
        for b in K["st_betas"]:
            dev_rates[b] = rate(dmv, dsc, dg, dt, dsel, c, {k: b * x for k, x in base_adds.items()})
            if dev_rates[b] >= 0.5:
                beta = b; break
        N = beta * tot1
        yb = Yd[delig, IDX[f"block_now_c{c}"]]
        X10 = Dd["resid"][torch.as_tensor(delig), pts.index(10)].float()
        u = X10[torch.as_tensor(yb)].mean(0) - X10[torch.as_tensor(~yb)].mean(0)
        u = u / u.norm()
        lays = [O.unpid(int(p), Fd)[0] for p in chosen[c]]
        rp = []
        for l in sorted(set(lays)):
            pool = np.flatnonzero(used & (np.repeat(np.arange(L), 2 * Fd) == l))
            pool = np.setdiff1d(pool, chosen[c])
            rp += list(rng.choice(pool, lays.count(l), replace=False))
        r_adds, _ = pole_adds(rp, total=N)
        res = {"beta": beta, "total_norm": N, "dev_rates": dev_rates,
               "unsteered": rate(tmv, tsc, tg, tt, tsel, c, {}),
               "neurons": rate(tmv, tsc, tg, tt, tsel, c, {k: beta * x for k, x in base_adds.items()}),
               "trained_direction": rate(tmv, tsc, tg, tt, tsel, c, {10: N * u}),
               "random_poles": rate(tmv, tsc, tg, tt, tsel, c, r_adds), "n_test": int(len(tsel))}
        v7["columns"][c] = res
        log(f"V7 col {c}: beta {beta} base {res['unsteered']:.3f} neurons {res['neurons']:.3f} trained {res['trained_direction']:.3f} "
            f"random {res['random_poles']:.3f}")
    cs = list(v7["columns"].values())
    mn, mt = np.mean([x["neurons"] for x in cs]), np.mean([x["trained_direction"] for x in cs])
    mr = np.mean([x["random_poles"] - x["unsteered"] for x in cs])
    v7["v_10"] = {"mean_neurons": float(mn), "mean_trained": float(mt), "mean_random_minus_unsteered": float(mr),
                  "mean_unsteered": float(np.mean([x["unsteered"] for x in cs])), "holds": bool(mn >= mt - 0.10 and abs(mr) <= 0.05)}
    out = {"study": "(v) V6-V7", "smoke": SMOKE, "V6": v6, "V7": v7, "seconds": round(time.time() - t0, 1)}
    OUT.write_text(json.dumps(out, indent=1, default=float))
    provenance.write(OUT, K)
    log("done", json.dumps({"v_9": v6["v_9"], "v_10": v7["v_10"]}))


if __name__ == "__main__":
    main()
