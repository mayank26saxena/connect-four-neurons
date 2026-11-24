"""PLAN.md addendum (u): the vertical blocker end to end, and the data its demo needs.
Recomputes the vertical circuit V with the (s) rule, then tests (u-1) L0 H2's attention, (u-2) the 15 directions feeding the layer-5
readout R, (u-3) R as column alarms, (u-4) what the first direction of each layer tracks, (u-5) the three demo switches (mean-ablation at
every position) against random controls. Writes results/vertical_map.json, web/vertical.json (demo data) and web/reference_vertical.json
(PyTorch logits under each switch, for tests/check_vertical_port.js). SMOKE=1: wiring check. Run on a GPU host."""
import json
import os
import time

import numpy as np
import torch
import torch.nn.functional as F
from scipy.stats import spearmanr

from c4n import circuit as C
from c4n import config, ns, provenance
from c4n import tactics as T
from c4n.model import tokens_from_moves

CFG = config.load("circuit")
SMOKE = bool(os.environ.get("SMOKE"))
K = {**CFG, **(CFG["smoke"] if SMOKE else {})}
DEV = "cuda" if torch.cuda.is_available() else "cpu"
SEED = K["seed"]
ROOT = config.ROOT
OUT = config.results_dir(CFG) / ("vertical_map_smoke.json" if SMOKE else "vertical_map.json")
N_RAND = 3 if SMOKE else 20
HEAD = (0, 2)
KDIR = 3
THEIRS = ns.THEIRS


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# ---------------------------------------------------------------- helpers

@torch.no_grad()
def head_attention(model, tok, tt, layer, head):
    """Attention probabilities (B, T) of one layer-0 head from the query at position tt (layer 0 only: no hooks needed)."""
    assert layer == 0
    b = model.blocks[0]
    x = model.tok(tok) + model.pos(torch.arange(tok.shape[1], device=tok.device))
    h = b.n1(x)
    B, Tn, D = h.shape
    H = b.attn.n_head
    q, k, _ = b.attn.qkv(h).view(B, Tn, 3, H, D // H).permute(2, 0, 3, 1, 4)
    ar = torch.arange(B, device=tok.device)
    qi = q[ar, head, tt]                                    # (B, dh)
    sc = torch.einsum("bd,btd->bt", qi, k[:, head]) / (D // H) ** 0.5
    mask = torch.arange(Tn, device=tok.device)[None] > tt[:, None]
    return torch.softmax(sc.masked_fill(mask, -1e9), -1)


def run_capture(Pt, base, src, subspace, layer_out):
    """Last-position activations of `layer_out` in the `base` run with `subspace` patched from `src` (as Patcher.run)."""
    outs = []
    with torch.no_grad():
        for sl, tt, ar in Pt._batches():
            cap = {}

            def hook(l, a, g, u, sl=sl, tt=tt, ar=ar):
                if l in subspace:
                    a = a.clone(); U = subspace[l]; cur = a[ar, tt]
                    a[ar, tt] = cur + ((Pt.acts[src][sl, l] - cur) @ U) @ U.T
                if l == layer_out:
                    cap["a"] = a[ar, tt].clone()
                return a
            Pt.m(Pt.tok[base][sl], hook=hook)
            outs.append(cap["a"])
    return torch.cat(outs)


def orientation_of(pos, mask, op_w):
    opp = pos ^ mask
    kinds = np.stack([np.any([(C.winning_dir(opp, mask, d) & op_w) != 0 for d in ds], 0) for ds in C.DIRS.values()], 1)
    return np.where(kinds.sum(1) > 1, 3, kinds.argmax(1))


def block_sets(moves, lengths):
    """Must-block positions (>= 4 stones) as tactics-style sets, by orientation."""
    idx, B = C.block_positions(moves, lengths, K["min_stones"])
    o = orientation_of(B["pos"][idx], B["mask"][idx], B["op_w"][idx])
    out = {}
    for i, name in enumerate(C.ORIENT[:3]):
        j = idx[o == i]
        out[name] = {"idx": j, "good": B["block"][j], "bad": B["legal"][j] & ~B["block"][j], "legal": B["legal"][j],
                     "_g": B["g"], "_t": B["t"], "n_all": len(j)}
    return out


def dir_hook(U, mu):
    """Mean-ablate span(U[l]) at every position: a' = a + (mu_l - a U^T) U."""
    def hook(l, a, g, u):
        if l not in U:
            return a
        P = U[l].to(a.device)                     # (k, F)
        return a + (mu[l].to(a.device) - a @ P.T) @ P
    return hook


def neuron_mean_hook(ids, mean_a, Fd):
    ix = C.by_layer(ids, Fd, "cpu")

    def hook(l, a, g, u):
        if l not in ix:
            return a
        a = a.clone(); j = ix[l].to(a.device)
        a[..., j] = mean_a[l][j.cpu()].to(a.device)
        return a
    return hook


def opp_run_on_last_col(bs):
    """Consecutive opponent stones from the top of the last-move column, if the cell above is empty, else 0."""
    n = len(bs.t)
    out = np.zeros(n, dtype=np.int64)
    rows = np.arange(n)
    c = bs.last_col.astype(np.int64)
    h = bs.heights[rows, np.maximum(c, 0)].astype(np.int64)
    ok = (c >= 0) & (h < 6)
    run = np.zeros(n, dtype=np.int64)
    alive = ok.copy()
    for k in range(1, 7):
        r = h - k
        m = alive & (r >= 0)
        cell = np.where(m, bs.grid[rows, np.clip(r, 0, 5), np.maximum(c, 0)], -1)
        alive = m & (cell == THEIRS)
        run += alive
    out[ok] = run[ok]
    return out


def main():
    t0 = time.time()
    torch.manual_seed(SEED)
    rng = np.random.default_rng(SEED)
    model = ns.load_web_model(DEV)
    Fd = model.cfg["d_ff"]
    data = {sp: ns.load_games(sp, K["n_games"]) for sp in ("analysis", "val")}
    Pt = {}
    for sp, (mv, sc, ln) in data.items():
        P = C.block_pairs(mv, ln, SEED, K["max_pairs"], K["min_stones"])  # as in (s): the vertical subset of the same pairs
        Pt[sp] = C.Patcher(model, C.subset(P, P["orient"] == 0), DEV, K["bs"])
    D, V = Pt["analysis"], Pt["val"]
    res = {"smoke": SMOKE, "n_pairs": {"analysis": D.N, "val": V.N}, "gap": {"analysis": D.gap, "val": V.gap}}

    # vertical circuit (the (s) rule) and the readout R
    fc = C.find_circuit(D, K["n_exact"], K["circuit_share"], K["circuit_cap"])
    Vc = fc["circuit"]
    diff = (D.acts["clean"] - D.acts["corr"]).mean(0).cpu().numpy().ravel()
    pole = {f: (1 if diff[f] >= 0 else -1) for f in Vc}
    R = [f for f in Vc if f // Fd == 5]
    res["circuit"] = {"size": len(Vc), "compact": fc["compact"], "by_layer": {str(l): sum(f // Fd == l for f in Vc) for l in range(6)},
                      "confirm_effect": V.effect(V.run("clean", neurons=C.by_layer(Vc, Fd, DEV), src="corr")),
                      "neurons": [{"id": f, "layer": f // Fd, "neuron": f % Fd, "pole": "+" if pole[f] > 0 else "-", "exact_effect": fc["exact"][f]} for f in Vc]}
    res["readout_confirm_effect"] = V.effect(V.run("clean", neurons=C.by_layer(R, Fd, DEV), src="corr"))
    log("V", len(Vc), "R", len(R), res["circuit"]["by_layer"], "confirm", round(res["circuit"]["confirm_effect"], 3))

    # (u-1) attention of L0 H2 at the last position
    att = head_attention(model, V.tok["clean"], V.t, *HEAD).cpu().numpy()
    Pv = V.P
    same, unif, self_s, bos, same_opp, same_me = [], [], [], [], [], []
    for k in range(V.N):
        t = int(Pv["t"][k]); mv = Pv["clean"][k][:t]; c = mv[-1]
        cols = np.array([mv[s - 1] for s in range(1, t)])  # keys 1..t-1 = earlier moves (move s-1)
        idx = np.flatnonzero(cols == c) + 1
        par = (np.arange(1, t) - 1) % 2 == (t - 1) % 2      # True where the earlier move was made by the same player as the last move
        same.append(att[k, idx].sum()); unif.append(len(idx) / (t + 1)); self_s.append(att[k, t]); bos.append(att[k, 0])
        same_opp.append(att[k, idx[par[idx - 1]]].sum() if len(idx) else 0.0)
        same_me.append(att[k, idx[~par[idx - 1]]].sum() if len(idx) else 0.0)
    u1 = {"same_column_share": float(np.mean(same)), "uniform_baseline": float(np.mean(unif)), "self": float(np.mean(self_s)),
          "bos": float(np.mean(bos)), "same_column_opponent": float(np.mean(same_opp)), "same_column_mover": float(np.mean(same_me))}
    u1["holds"] = bool(u1["same_column_share"] >= 0.5)
    res["u1_attention"] = u1
    log("u1", u1)

    # directions (layers 0-4, top 3 each) fitted on discovery
    U = {}
    for l in range(5):
        X = (D.acts["clean"][:, l] - D.acts["corr"][:, l]).float()
        _, S, Vh = torch.linalg.svd(X, full_matrices=False)
        U[l] = Vh[:KDIR].contiguous()
    sub = {l: U[l].T.contiguous() for l in U}
    res["directions_confirm_effect"] = V.effect(V.run("clean", subspace=sub, src="corr"))

    # (u-2) how much of R's clean-minus-corrupted change the 15 directions account for
    Rl = torch.as_tensor([f % Fd for f in R], device=DEV)
    a_c, a_r = V.acts["clean"][:, 5][:, Rl], V.acts["corr"][:, 5][:, Rl]
    a_p = run_capture(V, "clean", "corr", sub, 5)[:, Rl]
    moved = ((a_c.mean(0) - a_p.mean(0)) / (a_c.mean(0) - a_r.mean(0))).cpu().numpy()
    w = np.array([fc["exact"][f] for f in R])
    res["u2_readout_moved"] = {"weighted_mean": float((moved * w).sum() / w.sum()), "per_neuron": moved.round(4).tolist()}
    res["u2_readout_moved"]["holds"] = bool(res["u2_readout_moved"]["weighted_mean"] >= 0.7)
    log("u2", round(res["u2_readout_moved"]["weighted_mean"], 3))

    # (u-3) column alarms: effect by block column (confirmation) vs promoted column (direct logit)
    alarms = []
    for f in R:
        mg = V.run("clean", neurons=C.by_layer([f], Fd, DEV), src="corr")
        dl = V.base["clean"] - mg
        by = {}
        for c in range(7):
            m = Pv["block_col"] == c
            if m.sum() >= 10:
                by[c] = float(dl[m].mean() / (V.base["clean"][m].mean() - V.base["corr"][m].mean()))
        wv = model.blocks[5].mlp.down.weight[:, f % Fd] * model.nf.w
        dla = (model.head.weight @ wv).detach().cpu().numpy(); dla = dla - dla.mean()
        prom = int(np.argmax(dla * pole[f]))
        best = max(by, key=by.get) if by else None
        alarms.append({"id": f, "neuron": f % Fd, "pole": "+" if pole[f] > 0 else "-", "promotes": prom, "best_block_col": best,
                       "effect_by_col": by, "dla": dla.round(4).tolist(), "exact_effect": fc["exact"][f]})
    share = float(np.mean([a["promotes"] == a["best_block_col"] for a in alarms])) if alarms else None
    res["u3_alarms"] = {"share_promote_equals_best_col": share, "holds": bool(share is not None and share >= 0.8), "neurons": alarms}
    log("u3", share)

    # (u-4) meaning of the first direction of each layer, on all confirmation positions with >= 4 stones
    mv, sc, ln = data["val"]
    bs = ns.BoardSet(mv, ln)
    el = ns.eligible(ln, 4)
    feat = opp_run_on_last_col(bs)
    proj = {l: [] for l in range(5)}
    with torch.no_grad():
        for i in range(0, len(ln), 512):
            tok = tokens_from_moves(torch.as_tensor(mv[i:i + 512])).to(DEV)
            valid = torch.arange(42, device=DEV)[None] < torch.as_tensor(ln[i:i + 512], device=DEV)[:, None]

            def hook(l, a, g, u):
                if l < 5:
                    proj[l].append((a[:, :42][valid] @ U[l][0]).cpu())
                return a
            model(tok, hook=hook)
    rho = {}
    for l in range(5):
        p = torch.cat(proj[l]).numpy()
        rho[str(l)] = float(spearmanr(p[el], feat[el]).statistic)
    res["u4_direction_meaning"] = {"feature": "opponent run on top of the last-move column (cell above empty)", "spearman": rho,
                                   "feature_counts": {str(k): int((feat[el] == k).sum()) for k in range(4)},
                                   "holds": bool(sum(abs(v) >= 0.5 for v in rho.values()) >= 3)}
    log("u4", rho)

    # (u-5) demo switches: mean-ablation at every position
    mean_a, mean_y = T.means(model, data["analysis"][0], data["analysis"][2], DEV)
    mu = {l: (mean_a[l].to(DEV) @ U[l].T) for l in U}
    sets = block_sets(mv, ln)
    ctrl = T.control_set(mv, ln, sc, K["control_n"], SEED)

    def rates(hook=None, ahook=None):
        r = {o: T.rate(model, mv, s, DEV, hook=hook, attn_hook=ahook) for o, s in sets.items()}
        r["control"] = T.rate(model, mv, ctrl, DEV, hook=hook, attn_hook=ahook)
        return r
    base = rates()
    sw = {"none": base,
          "head": rates(ahook=T.head_mean_hook(*HEAD, mean_y)),
          "directions": rates(hook=dir_hook(U, mu)),
          "readout": rates(hook=neuron_mean_hook(R, mean_a, Fd))}
    rnd_dirs, rnd_R = [], []
    for _ in range(N_RAND):
        Ur = {l: torch.linalg.qr(torch.as_tensor(rng.standard_normal((Fd, KDIR)), dtype=torch.float32, device=DEV))[0].T.contiguous() for l in range(5)}
        mur = {l: (mean_a[l].to(DEV) @ Ur[l].T) for l in Ur}
        rnd_dirs.append(rates(hook=dir_hook(Ur, mur)))
        pool = np.setdiff1d(np.arange(5 * Fd, 6 * Fd), np.array(Vc))
        rnd_R.append(rates(hook=neuron_mean_hook(list(rng.choice(pool, len(R), replace=False)), mean_a, Fd)))
    med = lambda rs, k: float(np.median([r[k] for r in rs]))
    drop = lambda s, k: base[k] - sw[s][k]
    u5 = {"accuracy": sw, "n_positions": {o: int(len(s["idx"])) for o, s in sets.items()} | {"control": int(len(ctrl["idx"]))},
          "random_directions_median": {k: med(rnd_dirs, k) for k in base}, "random_readout_median": {k: med(rnd_R, k) for k in base}}
    u5["i_holds"] = bool(drop("head", "vertical") - drop("head", "control") >= 0.20)
    u5["ii_holds"] = bool(drop("directions", "vertical") >= 0.30 and drop("directions", "control") <= 0.10
                          and base["vertical"] - u5["random_directions_median"]["vertical"] <= 0.05)
    u5["iii_holds"] = bool(drop("readout", "vertical") >= 0.30 and drop("readout", "control") <= 0.05
                           and base["vertical"] - u5["random_readout_median"]["vertical"] <= 0.05)
    res["u5_switches"] = u5
    log("u5", {k: {kk: round(vv, 3) for kk, vv in v.items()} for k, v in sw.items()}, u5["i_holds"], u5["ii_holds"], u5["iii_holds"])

    # demo data
    pp = {}
    with torch.no_grad():
        S_R, S_D = [], {l: [] for l in range(5)}
        dmv, _, dln = data["analysis"]
        for i in range(0, min(len(dln), 2000), 512):
            tok = tokens_from_moves(torch.as_tensor(dmv[i:i + 512])).to(DEV)
            valid = torch.arange(42, device=DEV)[None] < torch.as_tensor(dln[i:i + 512], device=DEV)[:, None]

            def hook(l, a, g, u):
                x = a[:, :42][valid]
                if l < 5:
                    S_D[l].append((x @ U[l][0]).cpu())
                if l == 5:
                    S_R.append(x[:, Rl].cpu())
                return a
            model(tok, hook=hook)
        SR = torch.cat(S_R).numpy() * np.array([pole[f] for f in R])[None]
        pp["readout_p99"] = np.percentile(SR, 99, axis=0).round(4).tolist()
        pp["dir_p1_p99"] = {str(l): np.percentile(torch.cat(S_D[l]).numpy(), [1, 99]).round(4).tolist() for l in range(5)}
    # sign of each first direction: oriented so that positive = more like a vertical threat
    sgn = {l: float(np.sign(((D.acts["clean"][:, l] - D.acts["corr"][:, l]).mean(0) @ U[l][0]).item()) or 1.0) for l in range(5)}
    ex = {}
    for c in range(7):
        ks = np.flatnonzero(Pv["block_col"] == c)
        if len(ks):
            k = int(ks[0]); t = int(Pv["t"][k])
            ex[f"vertical_c{c}"] = Pv["clean"][k][:t].tolist()
    for o in ("horizontal", "diagonal"):
        s = sets[o]
        if len(s["idx"]):
            j = int(s["idx"][0]); g, t = int(s["_g"][j]), int(s["_t"][j])
            ex[o] = mv[g, :t].tolist()
    demo = {"head": list(HEAD), "head_mean_y": mean_y[HEAD[0], HEAD[1]].tolist(),
            "directions": {str(l): {"U": U[l].cpu().numpy().round(6).tolist(), "mu": mu[l].cpu().numpy().round(6).tolist(),
                                    "sign": sgn[l]} for l in U},
            "readout": [{"layer": 5, "neuron": a["neuron"], "pole": a["pole"], "promotes": a["promotes"], "p99": pp["readout_p99"][i],
                         "mean": float(mean_a[5][a["neuron"]]), "effect": a["exact_effect"]} for i, a in enumerate(alarms)],
            "dir_p1_p99": pp["dir_p1_p99"], "switch_accuracy": sw, "random_directions_median": u5["random_directions_median"],
            "random_readout_median": u5["random_readout_median"], "n_positions": u5["n_positions"], "examples": ex,
            "attention": u1, "circuit_size": len(Vc), "readout_size": len(R)}
    if not SMOKE:
        (ROOT / "web" / "vertical.json").write_text(json.dumps(demo))
        # reference logits under each switch (float32 PyTorch on the fp16 weights) for the browser check
        refs = []
        hooks = {"none": (None, None), "head": (None, T.head_mean_hook(*HEAD, mean_y)), "directions": (dir_hook(U, mu), None),
                 "readout": (neuron_mean_hook(R, mean_a, Fd), None)}
        for name, moves in ex.items():
            tok = tokens_from_moves(torch.as_tensor(np.array([moves + [-1] * (42 - len(moves))], dtype=np.int8))).to(DEV)[:, : len(moves) + 1]
            r = {"name": name, "tokens": tok[0].tolist(), "logits": {}}
            with torch.no_grad():
                for sname, (hk, ah) in hooks.items():
                    r["logits"][sname] = model(tok, hook=hk, attn_hook=ah)[0].cpu().numpy().round(5).tolist()
                r["head_attention_last"] = head_attention(model, tok, torch.as_tensor([len(moves)], device=DEV), *HEAD)[0].cpu().numpy().round(5).tolist()
            refs.append(r)
        (ROOT / "web" / "reference_vertical.json").write_text(json.dumps(refs))
    res["seconds"] = round(time.time() - t0, 1)
    OUT.write_text(json.dumps(res, indent=1))
    provenance.write(OUT, {**K, "head": HEAD, "k_dir": KDIR, "n_random": N_RAND})
    log(f"wrote {OUT} in {res['seconds']}s")


if __name__ == "__main__":
    main()
