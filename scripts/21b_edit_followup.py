"""Exploratory follow-up to the edit test (PLAN.md addendum (i)): stronger board edits, edits at every read point, and
edits to the threat-cell representation. Same edits and selection/report split as 21_world_model.py.
Writes world_model_followup.json."""
import importlib.util
import sys
import json
import os
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
    mt, thr, tpos, tneg = {}, {}, {}, {}
    Y = np.concatenate([lab["thr_mine"], lab["thr_theirs"]], 1)
    for p in range(1, NP):
        mg = WM.margins(probes[p], X[teT, p], lab["rel"][te], DEV)
        mg = np.where(mg > 0, mg, np.nan)
        mt[p] = torch.as_tensor(np.nan_to_num(np.nanmedian(mg, 0), nan=1.0), device=DEV).float()
        Wt, bt = WM.fit_binary(X[trT, p], Y[train_pos], DEV, WC["probe_steps"], WC["probe_lr"], seed=SEED)
        thr[p] = (Wt, bt)
        s = (X[teT, p].to(DEV).float() @ Wt + bt).cpu().numpy()
        yt = Y[te]
        tpos[p] = torch.as_tensor([np.median(s[yt[:, k], k]) if yt[:, k].sum() >= 20 else 4.0 for k in range(84)], device=DEV).float()
        tneg[p] = torch.as_tensor([np.median(s[~yt[:, k], k]) for k in range(84)], device=DEV).float()
    print("probes ready", flush=True)

    # the same edits as 21_world_model.py (same rng draw)
    g_all, t_all = lab["g"], lab["t"]
    cand = np.where(te & (t_all >= WC["min_ply"]))[0]
    chosen = rng.choice(cand, min(WC["edit_positions"], len(cand)), replace=False)
    edits = [(int(i), kind, k, src, tgt, np_, nm) for i in chosen for kind, k, src, tgt, np_, nm in WM.candidate_edits(int(lab["pos"][i]), int(lab["mask"][i]))]
    E.lib()
    with Pool(os.cpu_count()) as pool:
        sc = pool.map(wm21.teacher, [(e[5], e[6]) for e in edits], chunksize=64)
    keep = [j for j, s in enumerate(sc) if s is not None and (np.array(s) != E.ILLEGAL).any()]
    edits = [edits[j] for j in keep]
    sc_edit = np.array([sc[j] for j in keep], dtype=np.int16)
    fi = np.array([e[0] for e in edits])
    sc_orig = scores[g_all[fi], t_all[fi]]
    best_o = np.stack([WM.best_set(s) for s in sc_orig]); best_e = np.stack([WM.best_set(s) for s in sc_edit])
    legal_e = sc_edit != E.ILLEGAL
    kinds = np.array([e[1] for e in edits])
    cells = torch.as_tensor([e[2] for e in edits], device=DEV)
    src = torch.as_tensor([e[3] for e in edits], device=DEV); tgt = torch.as_tensor([e[4] for e in edits], device=DEV)
    pe = np.array([e[5] for e in edits], dtype=np.uint64); me = np.array([e[6] for e in edits], dtype=np.uint64)
    po, mo = lab["pos"][fi], lab["mask"][fi]
    # threat labels (84) of the edited board and which of them changed
    thr_e = np.concatenate([WM.grid42(E.winning_cells(pe, me)), WM.grid42(E.winning_cells(pe ^ me, me))], 1)
    thr_o = np.concatenate([WM.grid42(E.winning_cells(po, mo)), WM.grid42(E.winning_cells(po ^ mo, mo))], 1)
    diff = thr_e != thr_o
    maxc = int(diff.sum(1).max())
    ch_idx = np.zeros((len(edits), maxc), np.int64); ch_ok = np.zeros((len(edits), maxc), bool); ch_lab = np.zeros((len(edits), maxc), bool)
    for j in range(len(edits)):
        ks = np.where(diff[j])[0]
        ch_idx[j, :len(ks)] = ks; ch_ok[j, :len(ks)] = True; ch_lab[j, :len(ks)] = thr_e[j, ks]
    print("edits", len(edits), "max changed threat cells", maxc, flush=True)

    def hook_for(sl, mode, p0, k, rand, rows, cols):
        cs, ss, ts = cells[sl], src[sl], tgt[sl]
        ci, co, cl = (torch.as_tensor(a[sl], device=DEV) for a in (ch_idx, ch_ok, ch_lab))
        rv = None
        if rand:
            gen = torch.Generator(device="cpu").manual_seed(SEED + sl.start)
            rv = torch.nn.functional.normalize(torch.randn(len(cs), D, generator=gen), dim=1).to(DEV)

        def hook(pt, x):
            if pt < p0 or (mode == "board_blocks" and pt % 2):
                return x
            xs = x[rows, cols].float()
            if mode.startswith("board"):
                P = probes[pt]
                a, u = WM.edit_alpha(xs, P.W[:, cs].permute(1, 0, 2), P.b[cs], ss, ts, k * mt[pt][cs])
                step = a[:, None] * u
            else:  # threat cells: set each changed threat logit to k x the median logit of its new label
                Wt, bt = thr[pt]
                step = torch.zeros_like(xs)
                for c in range(ci.shape[1]):
                    w = Wt[:, ci[:, c]].T  # (B, d)
                    target = torch.where(cl[:, c], k * tpos[pt][ci[:, c]], k * tneg[pt][ci[:, c]])
                    cur = ((xs + step) * w).sum(1) + bt[ci[:, c]]
                    step = step + (co[:, c] * (target - cur) / w.pow(2).sum(1))[:, None] * w
            if rv is not None:
                step = rv * step.norm(dim=1, keepdim=True)
            x = x.clone(); x[rows, cols] = (xs + step).to(x.dtype)
            return x
        return hook

    def run(mode, p0, k, rand=False, bs=1024):
        mv = []
        for a in range(0, len(edits), bs):
            sl = slice(a, a + bs); ii = fi[sl]
            tok = tokens_from_moves(torch.as_tensor(moves[g_all[ii]])).to(DEV)
            rows = torch.arange(len(ii), device=DEV); cols = torch.as_tensor(t_all[ii], device=DEV)
            with torch.no_grad():
                lg, _ = WM.run(model, tok, resid_hook=hook_for(sl, mode, p0, k, rand, rows, cols))
            lg = lg[rows, cols].float(); lg[~torch.as_tensor(legal_e[sl], device=DEV)] = -1e9
            mv.append(lg.argmax(1).cpu())
        return torch.cat(mv).numpy()

    ar = np.arange(len(edits))
    with torch.no_grad():
        clean = run("board", 99, 1)  # p0 beyond the last point: no edit
    clean_ok = best_o[ar, clean]
    changed = clean_ok & ~(best_o & best_e).any(1)
    same = clean_ok & best_e[ar, clean]
    half = g_all[fi] % 2 == 0
    has = lambda p, m: (E.winning_cells(p, m) & E.playable(m)) != 0
    sub = {"flip": kinds == "flip", "creates_win": has(pe, me) & ~has(po, mo), "creates_threat": has(pe ^ me, me) & ~has(po ^ mo, mo) & ~has(pe, me),
           "removes_threat": has(po ^ mo, mo) & ~has(pe ^ me, me) & ~has(pe, me)}
    sub["tactical"] = sub["creates_win"] | sub["creates_threat"] | sub["removes_threat"]

    def score(mv):
        hit = best_e[ar, mv]
        r = {s: {h: float(hit[changed & m & hm].mean()) for h, hm in (("select", half), ("report", ~half), ("all", np.ones_like(half)))} for s, m in sub.items()}
        r["preserve_flip"] = float(hit[same & sub["flip"]].mean())
        return r

    out = {"n_changed": {s: int((changed & m).sum()) for s, m in sub.items()}, "runs": []}
    grid = [("board_blocks", 2, k) for k in (2, 4, 8)] + [("board", p0, k) for p0 in (1, 3, 5) for k in (1, 2, 4, 8)] + \
           [("threat", p0, k) for p0 in (1, 3, 5) for k in (1, 2, 4)]
    for mode, p0, k in grid:
        r = {"mode": mode, "p0": p0, "k": k, "edit": score(run(mode, p0, k)), "random": score(run(mode, p0, k, rand=True))}
        out["runs"].append(r)
        print(mode, p0, k, "flip", round(r["edit"]["flip"]["all"], 3), round(r["random"]["flip"]["all"], 3),
              "tactical", round(r["edit"]["tactical"]["all"], 3), round(r["random"]["tactical"]["all"], 3), flush=True)
    for key, subset, modes in (("i_a", "flip", ("board", "board_blocks")), ("i_b", "tactical", ("threat",))):
        cands = [r for r in out["runs"] if r["mode"] in modes]
        best = max(cands, key=lambda r: r["edit"][subset]["select"])
        f, rr = best["edit"][subset]["report"], best["random"][subset]["report"]
        out[key] = {"chosen": {"mode": best["mode"], "p0": best["p0"], "k": best["k"]}, "follow": f, "random": rr, "holds": bool(f >= 0.5 and f - rr >= 0.3)}
    print("i_a", out["i_a"], "\ni_b", out["i_b"], flush=True)
    (rd / "world_model_followup.json").write_text(json.dumps(out, indent=1))
    provenance.write(rd / "world_model_followup.json", CFG)


if __name__ == "__main__":
    main()
