"""Q4: modes of computation within a pole, and how causal damage splits across them.

For a stratified random sample of poles (plus the best concept-matched poles, reported separately):
1. Firings: positions where the pole is beyond p97 (+) / p3 (-); at most `max_firings`, sampled with the run seed.
2. Inputs: exact decomposition of the neuron's gate and up pre-activations into upstream components
   (embeddings, attention heads, earlier neurons), c4n/trace.py. Keep the `top_components` components with the largest
   mean |contribution| for this pole; L2-normalise each firing's vector.
3. Subcircuits: Leiden (RBConfiguration) on the cosine kNN graph of those vectors; clusters under `min_cluster_frac`
   are folded into their nearest cluster.
4. Modes: subcircuits whose ground-truth concept-rate profiles correlate above `merge_corr` are merged (union-find).
   This stands in for the LLM judge that grouped subcircuits by meaning in Tigges et al.
5. Damage: for each firing, zero the neuron at that single position and sum KL(intact || ablated) over that and all
   later positions of the game. Mode damage share = summed damage of its firings / pole total.

Writes results/modes.json (per-pole records + summary).
"""
import json

import igraph as ig
import leidenalg
import numpy as np
import torch
import torch.nn.functional as F

from c4n import analysis as A
from c4n import config, provenance
from c4n.concepts import NAMES
from c4n.data import concepts_for, load_split
from c4n.model import load_checkpoint, tokens_from_moves
from c4n.trace import decompose, trace

CFG = config.load()
AC, MC = CFG["analysis"], CFG["modes"]
DEV = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
FIRE = AC["fire_pct"]
LEGAL = None


def legal_table(moves):
    """(G, 42, 7) bool: column c is playable before move s of game g."""
    oh = np.zeros(moves.shape + (7,), dtype=np.int16)
    g, t = np.nonzero(moves >= 0)
    oh[g, t, moves[g, t]] = 1
    before = np.cumsum(oh, 1) - oh
    return before < 6


@torch.no_grad()
def firing_damage(model, moves, lengths, legal_all, games, ts, layer, neuron, bs=512):
    out = np.zeros(len(games))
    for i in range(0, len(games), bs):
        g, t = games[i:i + bs], ts[i:i + bs]
        tok = tokens_from_moves(torch.as_tensor(moves[g])).to(DEV)
        ln = torch.as_tensor(lengths[g], device=DEV)
        tt = torch.as_tensor(t, device=DEV)
        base = model(tok)[:, :42]

        def hook(l, a, gg, u):
            if l != layer:
                return a
            a = a.clone()
            a[torch.arange(a.shape[0], device=DEV), tt, neuron] = 0.0
            return a

        abl = model(tok, hook=hook)[:, :42]
        legal = torch.as_tensor(legal_all[g], device=DEV)
        lp = F.log_softmax(base.masked_fill(~legal, -1e9), -1)
        la = F.log_softmax(abl.masked_fill(~legal, -1e9), -1)
        kl = (lp.exp() * (lp - la)).sum(-1)
        s = torch.arange(42, device=DEV)[None]
        keep = (s >= tt[:, None]) & (s < ln[:, None])
        out[i:i + bs] = (kl * keep).sum(1).cpu().numpy()
    return out


def leiden_clusters(X, k, resolution, seed):
    S = X @ X.T
    S.fill_diagonal_(-1)
    k = min(k, X.shape[0] - 1)
    w, j = S.topk(k, 1)
    src = np.repeat(np.arange(X.shape[0]), k)
    edges = list(zip(src.tolist(), j.cpu().numpy().reshape(-1).tolist()))
    g = ig.Graph(n=X.shape[0], edges=edges)
    g.es["weight"] = w.clamp_min(0).cpu().numpy().reshape(-1).tolist()
    g.simplify(combine_edges="sum")
    part = leidenalg.find_partition(g, leidenalg.RBConfigurationVertexPartition, weights="weight",
                                    resolution_parameter=resolution, seed=seed)
    return np.array(part.membership)


def fold_small(labels, X, min_size):
    labels = labels.copy()
    while True:
        ids, cnt = np.unique(labels, return_counts=True)
        small = ids[cnt < min_size]
        if len(small) == 0 or len(ids) == 1:
            break
        big = ids[cnt >= min_size] if (cnt >= min_size).any() else ids[[cnt.argmax()]]
        cent = torch.stack([F.normalize(X[torch.as_tensor(labels == b)].mean(0), dim=0) for b in big])
        for s in small:
            m = labels == s
            labels[m] = big[(X[torch.as_tensor(m)] @ cent.T).mean(0).argmax().item()]
    _, labels = np.unique(labels, return_inverse=True)
    return labels


def merge_by_concepts(labels, Cf, thresh):
    ids = np.unique(labels)
    prof = np.stack([Cf[labels == i].mean(0) for i in ids])
    parent = list(range(len(ids)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a

    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            pa, pb = prof[a], prof[b]
            if pa.std() > 0 and pb.std() > 0 and np.corrcoef(pa, pb)[0, 1] > thresh:
                parent[find(a)] = find(b)
    root = np.array([find(i) for i in range(len(ids))])
    _, modes = np.unique(root[labels], return_inverse=True)
    return modes


def analyse_pole(model, moves, lengths, gidx, tidx, acts, C, base_rate, l, n, side, thr, rng):
    a = acts[:, l, n].float().numpy()
    fire = np.flatnonzero(a > thr if side == "+" else a < thr)
    if len(fire) > MC["max_firings"]:
        fire = np.sort(rng.choice(fire, MC["max_firings"], replace=False))
    if len(fire) < MC["min_firings"]:
        return {"layer": l, "neuron": n, "pole": side, "threshold": float(thr), "n_firings": int(len(fire)), "skipped": "too few firings"}
    games, ts = gidx[fire], tidx[fire]
    ug, inv = np.unique(games, return_inverse=True)
    feats = []
    for i in range(0, len(ug), 256):
        sel = np.flatnonzero((inv >= i) & (inv < i + 256))
        tok = tokens_from_moves(torch.as_tensor(moves[ug[i:i + 256]])).to(DEV)
        tr = trace(model, tok)
        c, names = decompose(model, tr, l, n, torch.as_tensor(inv[sel] - i, device=DEV), torch.as_tensor(ts[sel], device=DEV))
        feats.append((sel, c.reshape(len(sel), -1).cpu()))
    X = torch.zeros((len(fire), feats[0][1].shape[1]))
    for sel, c in feats:
        X[torch.as_tensor(sel)] = c
    comp_names = [f"gate:{x}" for x in names] + [f"up:{x}" for x in names]
    top = X.abs().mean(0).topk(min(MC["top_components"], X.shape[1])).indices
    Xn = F.normalize(X[:, top], dim=1).to(DEV)
    sub = leiden_clusters(Xn, MC["knn"], MC["resolution"], CFG["seed"])
    sub = fold_small(sub, Xn, max(5, int(MC["min_cluster_frac"] * len(fire))))
    Cf = C[fire].astype(np.float32)
    modes = merge_by_concepts(sub, Cf, MC["merge_corr"])
    dmg = firing_damage(model, moves, lengths, LEGAL, games, ts, l, n)
    total = dmg.sum()
    recs = []
    for m in np.unique(modes):
        mm = modes == m
        rate = Cf[mm].mean(0)
        lift = np.where(base_rate > 0, rate / np.maximum(base_rate, 1e-9), 0) * (rate >= 0.5)
        topc = np.argsort(-lift)[:5]
        mean_c = X[torch.as_tensor(mm)][:, top].mean(0)
        topi = mean_c.abs().topk(5).indices
        recs.append({"size": int(mm.sum()), "damage_share": float(dmg[mm].sum() / total) if total > 0 else 0.0,
                     "concepts": [{"name": NAMES[k], "rate": round(float(rate[k]), 3), "lift": round(float(lift[k]), 2)} for k in topc if lift[k] > 0],
                     "top_inputs": [{"component": comp_names[top[i]], "mean": round(float(mean_c[i]), 4)} for i in topi]})
    recs.sort(key=lambda r: -r["damage_share"])
    return {"layer": l, "neuron": n, "pole": side, "threshold": float(thr), "n_firings": int(len(fire)),
            "n_subcircuits": int(len(np.unique(sub))), "n_modes": len(recs), "mean_damage": float(dmg.mean()),
            "top_mode_share": recs[0]["damage_share"], "modes": recs}


def stats(poles):
    skipped = sum("skipped" in p for p in poles)
    poles = [p for p in poles if "skipped" not in p]
    nm = np.array([p["n_modes"] for p in poles]); ns = np.array([p["n_subcircuits"] for p in poles])
    top = np.array([p["top_mode_share"] for p in poles])
    multi = top[nm > 1]
    return {"n_poles": len(poles), "n_skipped": skipped, "modes_median": float(np.median(nm)), "modes_mean": float(nm.mean()),
            "subcircuits_median": float(np.median(ns)), "subcircuits_mean": float(ns.mean()),
            "share_single_mode": float((nm == 1).mean()), "share_top_mode_ge_0.9": float((top >= 0.9).mean()),
            "multi_mode_median_damage_outside_main": float(np.median(1 - multi)) if len(multi) else None,
            "modes_hist": np.bincount(nm).tolist()}


def main():
    rng = np.random.default_rng(CFG["seed"])
    model = load_checkpoint(config.ROOT / AC["checkpoint"], DEV)
    moves, scores, lengths = load_split(CFG, "analysis")
    n = AC["n_games"]
    moves, lengths = moves[:n], lengths[:n]
    C = concepts_for(CFG, "analysis", n)
    base_rate = C.mean(0)
    gidx, tidx = A.valid_index(lengths)
    global LEGAL
    LEGAL = legal_table(moves)
    acts, _, _ = A.collect(model, moves, lengths, DEV)
    hi, lo = A.percentiles(acts, [FIRE, 100 - FIRE], DEV)
    L, Fd = acts.shape[1], acts.shape[2]
    sample = []
    for l in range(L):
        for nn in rng.choice(Fd, MC["n_per_layer"] // 2, replace=False):
            sample += [(l, int(nn), "+"), (l, int(nn), "-")]
    featured = []
    pt = config.results_dir(CFG) / "pole_table.json"
    if pt.exists():
        rows = json.loads(pt.read_text())
        for l in range(L):
            best = sorted([r for r in rows if r["layer"] == l], key=lambda r: -r["f1_sweep"])[:MC["featured_per_layer"]]
            featured += [(r["layer"], r["neuron"], r["pole"]) for r in best]
    out = {"random_sample": [], "featured": []}
    for key, poles in (("random_sample", sample), ("featured", featured)):
        for i, (l, nn, s) in enumerate(poles):
            thr = hi[l, nn] if s == "+" else lo[l, nn]
            out[key].append(analyse_pole(model, moves, lengths, gidx, tidx, acts, C, base_rate, l, nn, s, float(thr), rng))
            if i % 20 == 0:
                print(key, i, len(poles), flush=True)
    out["summary_random_sample"] = stats(out["random_sample"])
    out["summary_by_layer"] = [stats([p for p in out["random_sample"] if p["layer"] == l]) for l in range(L)]
    if out["featured"]:
        out["summary_featured"] = stats(out["featured"])
    path = config.results_dir(CFG) / "modes.json"
    path.write_text(json.dumps(out, indent=1))
    provenance.write(path, CFG)
    print(json.dumps(out["summary_random_sample"], indent=1))


if __name__ == "__main__":
    main()
