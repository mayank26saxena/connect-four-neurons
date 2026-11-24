"""Is the board used? Colour-flip edits at the current position, at the history positions, or at all positions (PLAN.md
addendum (j)). Writes world_model_history.json. EDIT_POSITIONS=60 gives a smoke run."""
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
SMOKE = "EDIT_POSITIONS" in os.environ
MINE, THEIRS = WM.MINE, WM.THEIRS


def main():
    rd = config.results_dir(CFG)
    torch.manual_seed(SEED)
    rng = np.random.default_rng(SEED)
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
    X, res, probes = wm21.fit_all(model, moves, lengths, lab, train_pos, list(range(NP)), frames=("rel",))
    mt = {}
    for p in range(1, NP):
        mg = WM.margins(probes[p], X[teT, p], lab["rel"][te], DEV)
        mg = np.where(mg > 0, mg, np.nan)
        mt[p] = torch.as_tensor(np.nan_to_num(np.nanmedian(mg, 0), nan=1.0), device=DEV).float()
    # mean residual per read point, cell and relative state (training games)
    oh = torch.nn.functional.one_hot(torch.as_tensor(lab["rel"][train_pos]).long().to(DEV), 3).float()  # (N, 42, 3)
    cnt = oh.sum(0).clamp_min(1)
    means = torch.stack([torch.einsum("nkc,nd->kcd", oh, X[trT, p].to(DEV).float()) / cnt[..., None] for p in range(NP)])  # (NP, 42, 3, D)
    print("probes and mean directions ready", flush=True)

    g_all, t_all = lab["g"], lab["t"]
    cand = np.where(te & (t_all >= WC["min_ply"]))[0]
    chosen = rng.choice(cand, min(int(os.environ.get("EDIT_POSITIONS", WC["edit_positions"])), len(cand)), replace=False)
    edits, fill = [], []
    for i in chosen:
        g, t = g_all[i], t_all[i]
        for kind, k, src, tgt, np_, nm in WM.candidate_edits(int(lab["pos"][i]), int(lab["mask"][i])):
            if kind != "flip":
                continue
            occ = np.where(moves[g, :t] == k % 7)[0]
            edits.append((int(i), kind, k, src, tgt, np_, nm)); fill.append(int(occ[k // 7]))
    E.lib()
    with Pool(os.cpu_count()) as pool:
        sc = pool.map(wm21.teacher, [(e[5], e[6]) for e in edits], chunksize=64)
    keep = [j for j, s in enumerate(sc) if s is not None and (np.array(s) != E.ILLEGAL).any()]
    edits = [edits[j] for j in keep]; fill = np.array([fill[j] for j in keep])
    sc_edit = np.array([sc[j] for j in keep], dtype=np.int16)
    fi = np.array([e[0] for e in edits]); cells_np = np.array([e[2] for e in edits])
    sc_orig = scores[g_all[fi], t_all[fi]]
    best_o = np.stack([WM.best_set(s) for s in sc_orig]); best_e = np.stack([WM.best_set(s) for s in sc_edit])
    legal_e = sc_edit != E.ILLEGAL
    ar = np.arange(len(edits))
    pe = np.array([e[5] for e in edits], dtype=np.uint64); me = np.array([e[6] for e in edits], dtype=np.uint64)
    po, mo = lab["pos"][fi], lab["mask"][fi]
    has = lambda p, m: (E.winning_cells(p, m) & E.playable(m)) != 0
    print("flip edits", len(edits), flush=True)

    BS = 1024
    cache = {}

    def pairs(a, scope):
        key = (a, scope)
        if key not in cache:
            rows, cols, cl, sr, tg = [], [], [], [], []
            for b, e in enumerate(range(a, min(a + BS, len(edits)))):
                j, t = fill[e], t_all[fi[e]]
                for tp in {"all": range(j + 1, t + 1), "history": range(j + 1, t), "current": [t]}[scope]:
                    s = MINE if (j % 2) == (tp % 2) else THEIRS  # the stone's state relative to the mover at tp
                    rows.append(b); cols.append(tp); cl.append(cells_np[e]); sr.append(s); tg.append(THEIRS if s == MINE else MINE)
            cache[key] = tuple(torch.as_tensor(np.array(v, dtype=np.int64), device=DEV) for v in (rows, cols, cl, sr, tg))
        return cache[key]

    def run(scope, mode, p0, k, rand=False):
        out = []
        for a in range(0, len(edits), BS):
            ii = fi[a:a + BS]
            tok = tokens_from_moves(torch.as_tensor(moves[g_all[ii]])).to(DEV)
            rows, cols, cl, sr, tg = pairs(a, scope)
            rv = None
            if rand and len(rows):
                gen = torch.Generator(device="cpu").manual_seed(SEED + a)
                rv = torch.nn.functional.normalize(torch.randn(len(rows), D, generator=gen), dim=1).to(DEV)

            def hook(pt, x):
                if pt < p0 or pt == 0 or len(rows) == 0:
                    return x
                xs = x[rows, cols].float()
                if mode == "probe":
                    P = probes[pt]
                    al, u = WM.edit_alpha(xs, P.W[:, cl].permute(1, 0, 2), P.b[cl], sr, tg, k * mt[pt][cl])
                    step = al[:, None] * u
                else:
                    step = k * (means[pt][cl, tg] - means[pt][cl, sr])
                if rv is not None:
                    step = rv * step.norm(dim=1, keepdim=True)
                x = x.clone(); x[rows, cols] = (xs + step).to(x.dtype)
                return x
            r = torch.arange(len(ii), device=DEV); c = torch.as_tensor(t_all[ii], device=DEV)
            with torch.no_grad():
                lg, _ = WM.run(model, tok, resid_hook=hook)
            lg = lg[r, c].float(); lg[~torch.as_tensor(legal_e[a:a + BS], device=DEV)] = -1e9
            out.append(lg.argmax(1).cpu())
        return torch.cat(out).numpy()

    clean = run("current", "probe", 99, 1)
    clean_ok = best_o[ar, clean]
    changed = clean_ok & ~(best_o & best_e).any(1)
    same = clean_ok & best_e[ar, clean]
    half = g_all[fi] % 2 == 0
    sub = {"all_flips": np.ones(len(edits), bool), "creates_win": has(pe, me) & ~has(po, mo),
           "creates_threat": has(pe ^ me, me) & ~has(po ^ mo, mo) & ~has(pe, me), "removes_threat": has(po ^ mo, mo) & ~has(pe ^ me, me) & ~has(pe, me)}

    def score(mv):
        hit = best_e[ar, mv]
        r = {s: {h: float(hit[changed & m & hm].mean()) for h, hm in (("select", half), ("report", ~half), ("all", np.ones_like(half)))} for s, m in sub.items()}
        r["preserve"] = {"select": float(hit[same & half].mean()), "report": float(hit[same & ~half].mean())}
        return r

    out = {"n_edits": len(edits), "n_changed": {s: int((changed & m).sum()) for s, m in sub.items()}, "n_same": int(same.sum()), "runs": []}
    modes, p0s, ks = (("probe", "meandiff"), (1, 3), (1, 2, 4)) if not SMOKE else (("probe", "meandiff"), (1,), (2,))
    for scope in ("all", "history", "current"):
        for mode in modes:
            for p0 in p0s:
                for k in ks:
                    r = {"scope": scope, "mode": mode, "p0": p0, "k": k, "edit": score(run(scope, mode, p0, k)), "random": score(run(scope, mode, p0, k, rand=True))}
                    out["runs"].append(r)
                    print(scope, mode, p0, k, "follow", round(r["edit"]["all_flips"]["all"], 3), "random", round(r["random"]["all_flips"]["all"], 3),
                          "preserve", round(r["edit"]["preserve"]["select"], 3), flush=True)
    allr = [r for r in out["runs"] if r["scope"] == "all"]
    best = max(allr, key=lambda r: r["edit"]["all_flips"]["select"])
    cfg = (best["mode"], best["p0"], best["k"])
    pick = lambda scope: next(r for r in out["runs"] if (r["scope"], r["mode"], r["p0"], r["k"]) == (scope, *cfg))
    rep = lambda r: {"follow": r["edit"]["all_flips"]["report"], "random": r["random"]["all_flips"]["report"], "preserve": r["edit"]["preserve"]["report"]}
    out["chosen"] = {"mode": cfg[0], "p0": cfg[1], "k": cfg[2]}
    out["j_a"] = {**rep(best), "holds": bool(rep(best)["follow"] >= 0.5 and rep(best)["follow"] - rep(best)["random"] >= 0.3 and rep(best)["preserve"] >= 0.7)}
    out["j_b"] = {"history": rep(pick("history")), "current": rep(pick("current")), "all": rep(best)}
    out["j_b"]["holds"] = bool(out["j_b"]["history"]["follow"] > out["j_b"]["current"]["follow"])
    print("j_a", out["j_a"], "\nj_b", out["j_b"], flush=True)
    name = "world_model_history_smoke.json" if SMOKE else "world_model_history.json"
    (rd / name).write_text(json.dumps(out, indent=1))
    provenance.write(rd / name, CFG)


if __name__ == "__main__":
    main()
