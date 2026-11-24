"""Does the model keep a board in its head? W1-W6 of PLAN.md addendum (h). Writes world_model.json, world_model.npz and
the demo's web/worldmodel.json + web/worldmodel.bin (probe weights, puzzles)."""
import json
import os
from multiprocessing import Pool

import numpy as np
import torch

from c4n import config, provenance
from c4n import engine as E
from c4n import tactics as T
from c4n import worldmodel as WM
from c4n.data import load_split
from c4n.model import load_checkpoint, tokens_from_moves

CFG = config.load()
AC, WC = CFG["analysis"], CFG["worldmodel"]
DEV = "cuda" if torch.cuda.is_available() else "cpu"
SEED = CFG["seed"]


def teacher(args):
    pos, mask = args
    s = E.score_board(pos, mask, WC["teacher_depth"])
    return None if s is None else s.tolist()


def fit_all(model, moves, lengths, lab, train_pos, points, mlp=False, frames=("rel", "abs")):
    """Linear (and optionally MLP) board probes at each read point; returns scores and probes."""
    X = WM.collect_points(model, moves, lengths, DEV, points)
    tr, te = torch.as_tensor(train_pos), torch.as_tensor(~train_pos)
    trn, ten = train_pos, ~train_pos
    res, probes = {}, {}
    for i, p in enumerate(points):
        r = {}
        for fr in frames:
            P = WM.fit_linear(X[tr, i], lab[fr][trn], 3, DEV, WC["probe_steps"], WC["probe_lr"], seed=SEED)
            pred = WM.predict(P.logits, X[te, i], DEV)
            r[fr] = WM.board_scores(pred, lab[fr][ten])
            if fr == "rel":
                probes[p] = P
                r["rel_cell_acc"] = (pred == lab["rel"][ten]).mean(0).round(4).tolist()
        if mlp:
            fn = WM.fit_mlp(X[tr, i], lab["rel"][trn], 3, DEV, WC["mlp_hidden"], WC["mlp_steps"], seed=SEED)
            r["rel_mlp"] = WM.board_scores(WM.predict(fn, X[te, i], DEV), lab["rel"][ten])
        res[p] = r
    return X, res, probes


def main():
    rd = config.results_dir(CFG)
    torch.manual_seed(SEED)
    rng = np.random.default_rng(SEED)
    model = load_checkpoint(config.ROOT / AC["checkpoint"], DEV)
    L, Fd, Hh, D = model.cfg["n_layer"], model.cfg["d_ff"], model.cfg["n_head"], model.cfg["d_model"]
    moves, scores, lengths = load_split(CFG, "analysis")
    n = WC["n_games"]
    moves, scores, lengths = moves[:n], scores[:n], lengths[:n]
    lab = WM.board_labels(moves, lengths)
    n_train = int(WC["train_frac"] * n)
    train_pos = lab["g"] < n_train
    te = ~train_pos
    trT, teT = torch.as_tensor(train_pos), torch.as_tensor(te)
    names = WM.point_names(L)
    allp = list(range(2 * L + 1))
    out = {"points": names, "n_positions": [int(train_pos.sum()), int(te.sum())]}

    # ---- W1 board probes: trained model (all 13 points, MLP probe at block outputs) and untrained model ----
    X, res, probes = fit_all(model, moves, lengths, lab, train_pos, allp)
    for p in WM.block_points(L):
        fn = WM.fit_mlp(X[trT, p], lab["rel"][train_pos], 3, DEV, WC["mlp_hidden"], WC["mlp_steps"], seed=SEED)
        res[p]["rel_mlp"] = WM.board_scores(WM.predict(fn, X[teT, p], DEV), lab["rel"][te])
    out["probe"] = [res[p] for p in allp]
    base = WM.ply_baseline(lab["rel"][train_pos], lab["t"][train_pos], lab["rel"][te], lab["t"][te])
    out["ply_baseline"] = WM.board_scores(base, lab["rel"][te])
    m0 = load_checkpoint(config.ROOT / CFG["train"]["out_dir"] / "step_000000.pt", DEV)
    _, res0, _ = fit_all(m0, moves, lengths, lab, train_pos, WM.block_points(L), frames=("rel",))
    out["probe_untrained"] = {names[p]: res0[p]["rel"] for p in res0}
    del m0
    best = max(allp, key=lambda p: res[p]["rel"]["colour_acc"])
    out["best_point"] = names[best]
    print("W1", {names[p]: (round(res[p]["rel"]["colour_acc"], 3), round(res[p]["abs"]["colour_acc"], 3)) for p in allp}, flush=True)

    # ---- W2 threat cells ----
    thr = {}
    for p in WM.block_points(L):
        Y = np.concatenate([lab["thr_mine"], lab["thr_theirs"]], 1)
        Wt, bt = WM.fit_binary(X[trT, p], Y[train_pos], DEV, WC["probe_steps"], WC["probe_lr"], seed=SEED)
        s = (X[teT, p].to(DEV).float() @ Wt + bt).cpu().numpy()
        au = [WM.auroc(s[:, k], Y[te, k]) for k in range(84)]
        thr[p] = (Wt, bt)
        out.setdefault("threat_auroc", {})[names[p]] = {"mine": float(np.nanmean(au[:42])), "theirs": float(np.nanmean(au[42:]))}
    print("W2", out["threat_auroc"], flush=True)

    # target margins for edits: median held-out margin of correct predictions, per block-output point and cell
    mtarget = {}
    for p in WM.block_points(L)[1:]:
        mg = WM.margins(probes[p], X[teT, p], lab["rel"][te], DEV)
        mg = np.where(mg > 0, mg, np.nan)
        mtarget[p] = torch.as_tensor(np.nan_to_num(np.nanmedian(mg, 0), nan=1.0), device=DEV).float()

    # ---- W3 edits ----
    g_all, t_all = lab["g"], lab["t"]
    cand = np.where(te & (t_all >= WC["min_ply"]))[0]
    chosen = rng.choice(cand, min(WC["edit_positions"], len(cand)), replace=False)
    edits = []
    for i in chosen:
        for kind, k, src, tgt, np_, nm in WM.candidate_edits(int(lab["pos"][i]), int(lab["mask"][i])):
            edits.append((int(i), kind, k, src, tgt, np_, nm))
    E.lib()  # compile once before forking
    with Pool(os.cpu_count()) as pool:
        sc = pool.map(teacher, [(e[5], e[6]) for e in edits], chunksize=64)
    keep = [j for j, s in enumerate(sc) if s is not None and (np.array(s) != E.ILLEGAL).any()]
    edits = [edits[j] for j in keep]
    sc_edit = np.array([sc[j] for j in keep], dtype=np.int16)
    fi = np.array([e[0] for e in edits])
    sc_orig = scores[g_all[fi], t_all[fi]]
    best_o = np.stack([WM.best_set(s) for s in sc_orig])
    best_e = np.stack([WM.best_set(s) for s in sc_edit])
    legal_e = sc_edit != E.ILLEGAL
    kinds = np.array([e[1] for e in edits])
    cells = torch.as_tensor([e[2] for e in edits], device=DEV)
    src = torch.as_tensor([e[3] for e in edits], device=DEV)
    tgt = torch.as_tensor([e[4] for e in edits], device=DEV)
    print("W3 edits", len(edits), {k: int((kinds == k).sum()) for k in ("flip", "remove", "add")}, flush=True)

    def run_edits(start=0, only=None, rand=False, clean=False, bs=1024):
        """Greedy legal move (on the edited board's legal columns) and probabilities for every edit."""
        mv_out, pr_out = [], []
        for a in range(0, len(edits), bs):
            sl = slice(a, a + bs)
            ii = fi[sl]
            tok = tokens_from_moves(torch.as_tensor(moves[g_all[ii]])).to(DEV)
            rows = torch.arange(len(ii), device=DEV)
            cols = torch.as_tensor(t_all[ii], device=DEV)
            hook = None
            if not clean:
                rv = None
                if rand:
                    gen = torch.Generator(device="cpu").manual_seed(SEED + a)
                    rv = torch.nn.functional.normalize(torch.randn(len(ii), D, generator=gen), dim=1).to(DEV)
                hook = WM.edit_hook(probes, rows, cols, cells[sl], src[sl], tgt[sl], {p: mtarget[p][cells[sl]] for p in mtarget},
                                    start, rv, only)
            with torch.no_grad():
                lg, _ = WM.run(model, tok, resid_hook=hook)
            lg = lg[rows, cols].float()
            lg[~torch.as_tensor(legal_e[sl], device=DEV)] = -1e9
            mv_out.append(lg.argmax(1).cpu()); pr_out.append(torch.softmax(lg, 1).cpu())
        return torch.cat(mv_out).numpy(), torch.cat(pr_out).numpy()

    clean_mv, clean_pr = run_edits(clean=True)
    ar = np.arange(len(edits))
    clean_ok = best_o[ar, clean_mv]
    changed = clean_ok & ~(best_o & best_e).any(1)
    same = clean_ok & best_e[ar, clean_mv]
    half = (g_all[fi] % 2 == 0)  # selection half / report half, split by game
    w3 = {"n": {k: {"changed": int((changed & (kinds == k)).sum()), "same": int((same & (kinds == k)).sum())} for k in ("flip", "remove", "add")}}
    follow, keepr = {}, {}
    variants = {f"from_L{s}": dict(start=s) for s in range(L)}
    variants.update({f"only_L{s}": dict(only=s) for s in range(L)})
    variants.update({f"random_from_L{s}": dict(start=s, rand=True) for s in range(L)})
    mv_cache = {}
    for name, kw in variants.items():
        mv, pr = run_edits(**kw)
        mv_cache[name] = (mv, pr)
        hit = best_e[ar, mv]
        follow[name] = {k: {"all": float(hit[changed & (kinds == k)].mean()), "select": float(hit[changed & (kinds == k) & half].mean()),
                            "report": float(hit[changed & (kinds == k) & ~half].mean())} for k in ("flip", "remove", "add")}
        keepr[name] = {k: float(hit[same & (kinds == k)].mean()) for k in ("flip", "remove", "add")}
    nofollow = best_e[ar, clean_mv]
    w3["no_edit"] = {k: float(nofollow[changed & (kinds == k)].mean()) for k in ("flip", "remove", "add")}
    w3["follow"], w3["preserve"] = follow, keepr
    sel = max(range(L), key=lambda s: follow[f"from_L{s}"]["flip"]["select"])
    w3["chosen_start"] = sel
    w3["headline"] = {"follow": follow[f"from_L{sel}"]["flip"]["report"], "random": follow[f"random_from_L{sel}"]["flip"]["report"],
                      "no_edit": float(nofollow[changed & (kinds == "flip") & ~half].mean()), "preserve": keepr[f"from_L{sel}"]["flip"]}
    # tactical subsets: edit creates a win for the mover / creates a must-block / removes the need to block
    pe = np.array([e[5] for e in edits], dtype=np.uint64); me = np.array([e[6] for e in edits], dtype=np.uint64)
    po, mo = lab["pos"][fi], lab["mask"][fi]
    def has(p, m): return (E.winning_cells(p, m) & E.playable(m)) != 0
    sub = {"creates_win": has(pe, me) & ~has(po, mo), "creates_threat": has(pe ^ me, me) & ~has(po ^ mo, mo) & ~has(pe, me),
           "removes_threat": has(po ^ mo, mo) & ~has(pe ^ me, me) & ~has(pe, me)}
    hit = best_e[ar, mv_cache[f"from_L{sel}"][0]]
    hitr = best_e[ar, mv_cache[f"random_from_L{sel}"][0]]
    w3["tactical"] = {s: {"n": int((changed & m).sum()), "follow": float(hit[changed & m].mean()) if (changed & m).any() else None,
                          "random": float(hitr[changed & m].mean()) if (changed & m).any() else None} for s, m in sub.items()}
    out["W3"] = w3
    print("W3", w3["headline"], "start", sel, w3["tactical"], flush=True)

    # ---- W4 heads: ablation of the board probe at the best point, attention shares ----
    hg = np.arange(n_train, min(n, n_train + WC["head_games"]))
    hm, hl = moves[hg], lengths[hg]
    lab_h = WM.board_labels(hm, hl)
    mean_a, mean_y = T.means(model, moves[:n_train], lengths[:n_train], DEV)
    def acc_at(**kw):
        Xh = WM.collect_points(model, hm, hl, DEV, [best], **kw)[:, 0]
        return WM.board_scores(WM.predict(probes[best].logits, Xh, DEV), lab_h["rel"])
    intact = acc_at()
    heads = []
    for l in range(L):
        if 2 * l + 1 > best:
            break
        for h in range(Hh):
            r = acc_at(attn_hook=T.head_mean_hook(l, h, mean_y))
            heads.append({"layer": l, "head": h, "colour_drop": intact["colour_acc"] - r["colour_acc"], "empty_drop": intact["empty_acc"] - r["empty_acc"]})
    mlps = []
    for l in range(L):
        if 2 * l + 2 <= best:
            r = acc_at(mlp_hook=T.mlp_mean_hook(l, mean_a))
            mlps.append({"layer": l, "colour_drop": intact["colour_acc"] - r["colour_acc"], "empty_drop": intact["empty_acc"] - r["empty_acc"]})
    share = attention_shares(model, hm, hl)
    out["W4"] = {"intact": intact, "heads": heads, "mlps": mlps, "attention_share": share}
    print("W4 top heads", sorted(heads, key=lambda r: -r["colour_drop"])[:5], flush=True)

    # ---- W5 neurons in board terms ----
    maps = {k: np.zeros((L, Fd, 42), np.float16) for k in ("read_col", "read_emp", "write_col", "write_emp", "write_thr_mine", "write_thr_theirs")}
    for l in range(L):
        b = model.blocks[l]
        G = (b.mlp.gate.weight * b.n2.w[None]).detach()
        Dn = b.mlp.down.weight.detach().T  # (F, d)
        dc, de = WM.probe_dirs(probes[2 * l + 1])
        maps["read_col"][l] = WM.cos_map(G, dc).cpu().numpy(); maps["read_emp"][l] = WM.cos_map(G, de).cpu().numpy()
        dc, de = WM.probe_dirs(probes[2 * l + 2])
        maps["write_col"][l] = WM.cos_map(Dn, dc).cpu().numpy(); maps["write_emp"][l] = WM.cos_map(Dn, de).cpu().numpy()
        Wt = thr[2 * l + 2][0]
        maps["write_thr_mine"][l] = WM.cos_map(Dn, Wt[:, :42]).cpu().numpy(); maps["write_thr_theirs"][l] = WM.cos_map(Dn, Wt[:, 42:]).cpu().numpy()
    atlas = json.loads((rd / "tactic_atlas.json").read_text())
    w5 = {}
    for tac, key in (("block", "write_thr_theirs"), ("win", "write_thr_mine")):
        stat = np.abs(maps[key].astype(np.float32)).max(-1)  # (L, F)
        top = atlas["top_neurons"][tac]
        obs = float(np.median([stat[r["layer"], r["neuron"]] for r in top]))
        layers = np.array([r["layer"] for r in top])
        null = np.array([np.median(np.concatenate([stat[l, rng.choice(Fd, (layers == l).sum(), replace=False)] for l in np.unique(layers)]))
                         for _ in range(WC["n_perm"])])
        w5[tac] = {"median_top": obs, "median_random": float(np.median(null)), "p": float((null >= obs).mean())}
    out["W5"] = w5
    print("W5", w5, flush=True)
    np.savez_compressed(rd / "world_model.npz", **maps)

    # ---- W6 emergence ----
    em = []
    ng = WC["emergence_games"]
    sub_lab = {k: v[lab["g"] < ng] if isinstance(v, np.ndarray) else v for k, v in lab.items()}
    tr6 = sub_lab["g"] < int(WC["train_frac"] * ng)
    for step in CFG["tactics"]["emergence_ckpts"]:
        mk = load_checkpoint(config.ROOT / CFG["train"]["out_dir"] / f"step_{step:06d}.pt", DEV)
        _, r6, _ = fit_all(mk, moves[:ng], lengths[:ng], sub_lab, tr6, WM.block_points(L), frames=("rel",))
        em.append({"step": step, **{names[p]: r6[p]["rel"] for p in r6}})
        print("W6", step, {names[p]: round(r6[p]["rel"]["colour_acc"], 3) for p in r6}, flush=True)
    out["W6"] = em

    (rd / "world_model.json").write_text(json.dumps(out, indent=1))
    provenance.write(rd / "world_model.json", CFG)
    export_web(model, probes, thr, mtarget, sel, edits, changed, kinds, sub, best_o, best_e, sc_orig, sc_edit, clean_pr, mv_cache, fi, g_all, t_all, moves, rng)


@torch.no_grad()
def attention_shares(model, moves, lengths, bs=256):
    """Per (layer, head): attention share on the mover's own past moves, the opponent's past moves, and the start token,
    averaged over query positions t >= 2."""
    L, Hh = model.cfg["n_layer"], model.cfg["n_head"]
    acc = torch.zeros(L, Hh, 3, device=DEV); cnt = 0
    for i in range(0, len(lengths), bs):
        tok = tokens_from_moves(torch.as_tensor(moves[i:i + bs])).to(DEV)
        ln = torch.as_tensor(lengths[i:i + bs], device=DEV)
        T_ = tok.shape[1]
        tq = torch.arange(T_, device=DEV)
        qmask = (tq[None] >= 2) & (tq[None] < ln[:, None])  # (B, T)
        # key j >= 1 is move j-1, "mine" relative to query t iff (t - (j - 1)) is even
        mine = ((tq[:, None] - (tq[None] - 1)) % 2 == 0) & (tq[None] >= 1) & (tq[None] <= tq[:, None])
        theirs = ((tq[:, None] - (tq[None] - 1)) % 2 == 1) & (tq[None] >= 1) & (tq[None] <= tq[:, None])
        x = model.tok(tok) + model.pos(tq)
        for l, b in enumerate(model.blocks):
            h = b.n1(x)
            B_, _, Dm = h.shape
            q, k, v = b.attn.qkv(h).view(B_, T_, 3, Hh, Dm // Hh).permute(2, 0, 3, 1, 4)
            att = torch.softmax(q @ k.transpose(-1, -2) / (Dm // Hh) ** 0.5 + torch.triu(torch.full((T_, T_), -1e9, device=DEV), 1), -1)
            qm = qmask[:, None, :].float()
            acc[l, :, 0] += ((att * mine.float()).sum(-1) * qm).sum((0, 2))
            acc[l, :, 1] += ((att * theirs.float()).sum(-1) * qm).sum((0, 2))
            acc[l, :, 2] += (att[..., 0] * qm).sum((0, 2))
            x = b(x, l)
        cnt += int(qmask.sum())
    return (acc / cnt).cpu().numpy().round(4).tolist()


def export_web(model, probes, thr, mtarget, sel, edits, changed, kinds, sub, best_o, best_e, sc_orig, sc_edit, clean_pr, mv_cache, fi, g_all, t_all, moves, rng):
    """Probe weights at the block outputs (fp16) + target margins + puzzles for the demo; puzzles carry PyTorch
    probabilities so the JS port can be checked against them (tests/check_web_port.js)."""
    L = model.cfg["n_layer"]
    pts = WM.block_points(L)
    W = np.stack([probes[p].W.cpu().numpy() for p in pts]).astype(np.float16)            # (7, d, 42, 3)
    b = np.stack([probes[p].b.cpu().numpy() for p in pts]).astype(np.float32)            # (7, 42, 3)
    Wt = np.stack([thr[p][0].cpu().numpy() for p in pts]).astype(np.float16)             # (7, d, 84)
    bt = np.stack([thr[p][1].cpu().numpy() for p in pts]).astype(np.float32)             # (7, 84)
    web = config.ROOT / "web"
    blob = W.tobytes() + Wt.tobytes()
    (web / "worldmodel.bin").write_bytes(blob)
    mv, pr = mv_cache[f"from_L{sel}"]
    ar = np.arange(len(edits))
    puzzles = []
    for name, m in [("creates_win", sub["creates_win"]), ("creates_threat", sub["creates_threat"]), ("removes_threat", sub["removes_threat"]),
                    ("other", ~(sub["creates_win"] | sub["creates_threat"] | sub["removes_threat"]))]:
        idx = np.where(changed & (kinds == "flip") & m)[0]
        hit = idx[best_e[idx, mv[idx]]]
        miss = idx[~best_e[idx, mv[idx]]]
        take = list(rng.choice(hit, min(3, len(hit)), replace=False)) + list(rng.choice(miss, min(1, len(miss)), replace=False))
        for j in take:
            e = edits[j]; i = fi[j]
            puzzles.append({"type": name, "moves": moves[g_all[i], : t_all[i]].tolist(), "kind": e[1], "cell": e[2], "src": e[3], "tgt": e[4],
                            "best_real": np.where(best_o[j])[0].tolist(), "best_edit": np.where(best_e[j])[0].tolist(),
                            "scores_real": sc_orig[j].tolist(), "scores_edit": sc_edit[j].tolist(),
                            "p_clean": clean_pr[j].round(5).tolist(), "p_edit": pr[j].round(5).tolist(), "followed": bool(best_e[j, mv[j]])})
    # reference probabilities for the JS check, from a copy of the model and probes rounded to float16 as exported
    import copy
    m16 = copy.deepcopy(model)
    for prm in m16.parameters():
        prm.data = prm.data.half().float()
    pr16 = {p: WM.Probe(probes[p].W.half().float(), probes[p].b) for p in probes}
    for pz in puzzles:
        t = len(pz["moves"])
        tok = tokens_from_moves(torch.as_tensor(np.array([pz["moves"] + [-1] * (42 - t)], dtype=np.int8))).to(DEV)
        legal = torch.as_tensor(np.array(pz["scores_edit"]) != E.ILLEGAL, device=DEV)
        r, c = torch.zeros(1, dtype=torch.long, device=DEV), torch.full((1,), t, dtype=torch.long, device=DEV)
        k, a, b2 = (torch.full((1,), v, dtype=torch.long, device=DEV) for v in (pz["cell"], pz["src"], pz["tgt"]))
        for key, hook in (("p_clean", None), ("p_edit", WM.edit_hook(pr16, r, c, k, a, b2, {p: mtarget[p][k] for p in mtarget}, sel))):
            with torch.no_grad():
                lg, _ = WM.run(m16, tok, resid_hook=hook)
            lg = lg[0, t].float().masked_fill(~legal, -1e9)
            pz[key] = torch.softmax(lg, 0).cpu().numpy().round(5).tolist()
    meta = {"points": [WM.point_names(L)[p] for p in pts], "d": model.cfg["d_model"], "W_shape": list(W.shape), "Wt_shape": list(Wt.shape),
            "b": b.round(5).tolist(), "bt": bt.round(5).tolist(), "margin": [mtarget[p].cpu().numpy().round(4).tolist() for p in pts[1:]],
            "start": sel, "puzzles": puzzles}
    (web / "worldmodel.json").write_text(json.dumps(meta))
    print("web export", len(puzzles), "puzzles", flush=True)


if __name__ == "__main__":
    main()
