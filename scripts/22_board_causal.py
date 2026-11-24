"""Treatment-versus-control test of whether the move uses the board (PLAN.md addendum (k)), for the model named by
$C4N_CONFIG. Writes <results_dir>/board_causal.json. Teacher scores of the flips do not depend on the model and are cached in
data/edit_set.npz (built on first use). EDIT_POSITIONS=N overrides the number of positions (smoke run)."""
import importlib.util
import json
import os
import sys
from multiprocessing import Pool

import numpy as np
import torch

from c4n import config, provenance
from c4n import engine as E
from c4n import worldmodel as WM
from c4n.data import load_split
from c4n.model import load_checkpoint, tokens_from_moves

spec = importlib.util.spec_from_file_location("wm21", config.ROOT / "scripts" / "21_world_model.py")
wm21 = importlib.util.module_from_spec(spec); sys.modules["wm21"] = wm21; spec.loader.exec_module(wm21)
CFG, WC, DEV, SEED = wm21.CFG, wm21.WC, wm21.DEV, wm21.SEED
MINE, THEIRS = WM.MINE, WM.THEIRS
SMOKE = "EDIT_POSITIONS" in os.environ
N_POS = int(os.environ.get("EDIT_POSITIONS", 3000))
BS = 1024


def edit_set(lab, moves, scores):
    """All single-stone flips at N_POS held-out positions with teacher scores, plus one seeded (relevant, irrelevant) pair per
    position. Independent of the model; cached."""
    path = config.ROOT / "data" / ("edit_set_smoke.npz" if SMOKE else "edit_set.npz")
    if path.exists():
        return dict(np.load(path))
    rng = np.random.default_rng(SEED + 22)
    g_all, t_all = lab["g"], lab["t"]
    te = g_all >= int(WC["train_frac"] * WC["n_games"])
    cand = np.where(te & (t_all >= WC["min_ply"]))[0]
    chosen = rng.choice(cand, min(N_POS, len(cand)), replace=False)
    rows, boards = [], []
    for i in chosen:
        g, t = g_all[i], t_all[i]
        for kind, k, src, tgt, np_, nm in WM.candidate_edits(int(lab["pos"][i]), int(lab["mask"][i])):
            if kind == "flip":
                rows.append((int(i), k, src, tgt, int(np.where(moves[g, :t] == k % 7)[0][k // 7]))); boards.append((np_, nm))
    E.lib()
    with Pool(os.cpu_count()) as pool:
        sc = pool.map(wm21.teacher, boards, chunksize=64)
    ok = [j for j, s in enumerate(sc) if s is not None and (np.array(s) != E.ILLEGAL).any()]
    rows = np.array([rows[j] for j in ok]); sce = np.array([sc[j] for j in ok], dtype=np.int16)
    fi = rows[:, 0]
    best_o = np.stack([WM.best_set(s) for s in scores[g_all[fi], t_all[fi]]]); best_e = np.stack([WM.best_set(s) for s in sce])
    relevant = ~(best_o & best_e).any(1); irrelevant = (best_o == best_e).all(1)
    pr, pi_ = [], []
    for i in np.unique(fi):
        r, q = np.where((fi == i) & relevant)[0], np.where((fi == i) & irrelevant)[0]
        if len(r) and len(q):
            pr.append(rng.choice(r)); pi_.append(rng.choice(q))
    out = dict(fi=fi, cell=rows[:, 1], src=rows[:, 2], tgt=rows[:, 3], fill=rows[:, 4], sc_edit=sce, pair_rel=np.array(pr), pair_irr=np.array(pi_))
    np.savez_compressed(path, **out)
    print("edit set", len(rows), "flips,", len(pr), "pairs", flush=True)
    return out


def main():
    rd = config.results_dir(CFG)
    rd.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(SEED)
    model = load_checkpoint(config.ROOT / CFG["analysis"]["checkpoint"], DEV)
    L, D = model.cfg["n_layer"], model.cfg["d_model"]
    NP = 2 * L + 1
    moves, scores, lengths = load_split(CFG, "analysis")
    n = WC["n_games"]
    moves, scores, lengths = moves[:n], scores[:n], lengths[:n]
    lab = WM.board_labels(moves, lengths)
    train_pos = lab["g"] < int(WC["train_frac"] * n)
    te = ~train_pos
    trT, teT = torch.as_tensor(train_pos), torch.as_tensor(te)
    out = {"model": model.cfg, "checkpoint": CFG["analysis"]["checkpoint"]}
    X, res, probes = wm21.fit_all(model, moves, lengths, lab, train_pos, list(range(NP)), frames=("rel",))
    bestp = max(range(NP), key=lambda p: res[p]["rel"]["colour_acc"])
    out["board"] = {"best_point": wm21.WM.point_names(L)[bestp], "colour_acc": res[bestp]["rel"]["colour_acc"], "empty_acc": res[bestp]["rel"]["empty_acc"],
                    "by_point": {wm21.WM.point_names(L)[p]: res[p]["rel"]["colour_acc"] for p in range(NP)}}
    print("board", out["board"]["best_point"], round(out["board"]["colour_acc"], 3), flush=True)
    mt = {}
    for p in range(1, NP):
        mg = WM.margins(probes[p], X[teT, p], lab["rel"][te], DEV)
        mg = np.where(mg > 0, mg, np.nan)
        mt[p] = torch.as_tensor(np.nan_to_num(np.nanmedian(mg, 0), nan=1.0), device=DEV).float()
    oh = torch.nn.functional.one_hot(torch.as_tensor(lab["rel"][train_pos]).long().to(DEV), 3).float()
    cnt = oh.sum(0).clamp_min(1)
    means = torch.stack([torch.einsum("nkc,nd->kcd", oh, X[trT, p].to(DEV).float()) / cnt[..., None] for p in range(NP)])

    es = edit_set(lab, moves, scores)
    g_all, t_all = lab["g"], lab["t"]
    fi, cell_a, src_a, tgt_a, fill_a, sce = (es[k] for k in ("fi", "cell", "src", "tgt", "fill", "sc_edit"))
    best_o = np.stack([WM.best_set(s) for s in scores[g_all[fi], t_all[fi]]]); best_e = np.stack([WM.best_set(s) for s in sce])
    legal = scores[g_all[fi], t_all[fi]] != E.ILLEGAL
    idx = np.concatenate([es["pair_rel"], es["pair_irr"]]); P = len(es["pair_rel"])  # rows: P relevant, then P irrelevant
    out["n_pairs_built"] = P

    def run(rows_idx, p0, mode=None, k=1, rand=False):
        mv = []
        for a in range(0, len(rows_idx), BS):
            ei = rows_idx[a:a + BS]
            rr, cc, cl, sr, tg = [], [], [], [], []
            for b, e in enumerate(ei):
                j, t = fill_a[e], t_all[fi[e]]
                for tp in range(j + 1, t + 1):
                    s = MINE if (j % 2) == (tp % 2) else THEIRS
                    rr.append(b); cc.append(tp); cl.append(cell_a[e]); sr.append(s); tg.append(THEIRS if s == MINE else MINE)
            rows, cols, cl, sr, tg = (torch.as_tensor(np.array(v, dtype=np.int64), device=DEV) for v in (rr, cc, cl, sr, tg))
            rv = None
            if rand:
                gen = torch.Generator(device="cpu").manual_seed(SEED + a)
                rv = torch.nn.functional.normalize(torch.randn(len(rows), D, generator=gen), dim=1).to(DEV)

            def hook(pt, x):
                if mode is None or pt < p0 or pt == 0:
                    return x
                xs = x[rows, cols].float()
                if mode == "probe":
                    Pr = probes[pt]
                    al, u = WM.edit_alpha(xs, Pr.W[:, cl].permute(1, 0, 2), Pr.b[cl], sr, tg, k * mt[pt][cl])
                    step = al[:, None] * u
                else:
                    step = k * (means[pt][cl, tg] - means[pt][cl, sr])
                if rv is not None:
                    step = rv * step.norm(dim=1, keepdim=True)
                x = x.clone(); x[rows, cols] = (xs + step).to(x.dtype)
                return x
            tok = tokens_from_moves(torch.as_tensor(moves[g_all[fi[ei]]])).to(DEV)
            r = torch.arange(len(ei), device=DEV); c = torch.as_tensor(t_all[fi[ei]], device=DEV)
            with torch.no_grad():
                lg, _ = WM.run(model, tok, resid_hook=hook)
            lg = lg[r, c].float(); lg[~torch.as_tensor(legal[ei], device=DEV)] = -1e9
            mv.append(lg.argmax(1).cpu())
        return torch.cat(mv).numpy()

    clean = run(idx, 99)
    ok = best_o[idx[:P], clean[:P]]  # the clean model plays a teacher-best move at this position (rel and irr share it)
    out["n_pairs"] = int(ok.sum())
    half = (g_all[fi[idx[:P]]] % 2 == 0)
    ar = np.arange(P)

    def stats(mv, mask):
        mr, mi, cr, ci = mv[:P], mv[P:], clean[:P], clean[P:]
        chg_r, chg_i = mr != cr, mi != ci
        hit_r = best_e[idx[:P], mr]; keep_i = best_o[idx[P:], mi]
        m = ok & mask
        return {"n": int(m.sum()), "change_rel": float(chg_r[m].mean()), "change_irr": float(chg_i[m].mean()),
                "spec": float(chg_r[m].mean() - chg_i[m].mean()), "dir": float(hit_r[m & chg_r].mean()) if (m & chg_r).any() else float("nan"),
                "follow": float(hit_r[m].mean()), "keep_irr": float(keep_i[m].mean())}

    modes, p0s, ks = ("probe", "meandiff"), [p for p in (1, 3) if p < NP], (1, 2)
    runs = []
    for mode in modes:
        for p0 in p0s:
            for k in ks:
                mv = run(idx, p0, mode, k)
                rm = run(idx[:P], p0, mode, k, rand=True)
                rnd = {"change_rel": float((rm != clean[:P])[ok & ~half].mean()), "follow": float(best_e[idx[:P], rm][ok & ~half].mean())}
                runs.append({"mode": mode, "p0": p0, "k": k, "select": stats(mv, half), "report": stats(mv, ~half), "random_report": rnd})
                print(mode, p0, k, "select spec", round(runs[-1]["select"]["spec"], 3), "report spec", round(runs[-1]["report"]["spec"], 3),
                      "dir", round(runs[-1]["report"]["dir"], 3), "keep", round(runs[-1]["report"]["keep_irr"], 3), flush=True)
    out["runs"] = runs
    good = [r for r in runs if r["select"]["keep_irr"] >= 0.7] or runs
    best = max(good, key=lambda r: r["select"]["spec"])
    out["chosen"] = {k: best[k] for k in ("mode", "p0", "k")}
    mvb = run(idx, best["p0"], best["mode"], best["k"])
    rng = np.random.default_rng(SEED)
    gg = g_all[fi[idx[:P]]]
    ug = np.unique(gg[~half & ok])
    boots = []
    for _ in range(500):
        pick = rng.choice(ug, len(ug))
        sel = np.concatenate([np.where((gg == g) & ~half & ok)[0] for g in pick])
        boots.append(float((mvb[:P][sel] != clean[:P][sel]).mean() - (mvb[P:][sel] != clean[P:][sel]).mean()))
    out["result"] = {**best["report"], "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))], "random_report": best["random_report"]}
    out["verdict"] = {"readable_board": bool(out["board"]["colour_acc"] >= 0.9), "k_a": bool(best["report"]["spec"] >= 0.25 and out["result"]["ci95"][0] > 0 and best["report"]["dir"] >= 0.5 and best["report"]["keep_irr"] >= 0.7)}
    print("result", json.dumps(out["result"]), "\nverdict", out["verdict"], flush=True)
    (rd / ("board_causal_smoke.json" if SMOKE else "board_causal.json")).write_text(json.dumps(out, indent=1))
    provenance.write(rd / ("board_causal_smoke.json" if SMOKE else "board_causal.json"), CFG)


if __name__ == "__main__":
    main()
