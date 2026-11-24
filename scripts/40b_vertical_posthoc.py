"""Post-hoc, descriptive follow-up to PLAN (u) after (u-1) and (u-4) failed (not a test; nothing registered changes):
(a) where L0 H2 does put its attention from the last move (by player, column and recency);
(b) what the first direction of each of layers 0-4 tracks, as AUROC against binary board facts on confirmation positions (>= 4 stones).
Directions are refitted exactly as in scripts/40_vertical_map.py. Writes results/vertical_posthoc.json."""
import json
import importlib.util
import sys

import numpy as np
import torch
from sklearn.metrics import roc_auc_score

from c4n import circuit as C
from c4n import config, ns, provenance
from c4n.model import tokens_from_moves

spec = importlib.util.spec_from_file_location("vm40", config.ROOT / "scripts" / "40_vertical_map.py")
vm = importlib.util.module_from_spec(spec); sys.modules["vm40"] = vm; spec.loader.exec_module(vm)
K, DEV, SEED = vm.K, vm.DEV, vm.SEED


def main():
    torch.manual_seed(SEED)
    model = ns.load_web_model(DEV)
    data = {sp: ns.load_games(sp, K["n_games"]) for sp in ("analysis", "val")}
    Pt = {}
    for sp, (mv, sc, ln) in data.items():
        P = C.block_pairs(mv, ln, SEED, K["max_pairs"], K["min_stones"])
        Pt[sp] = C.Patcher(model, C.subset(P, P["orient"] == 0), DEV, K["bs"])
    D, V = Pt["analysis"], Pt["val"]
    out = {"posthoc": True}
    # (a) attention breakdown on clean vertical confirmation pairs, and on all confirmation positions with >= 4 stones
    def breakdown(tok, tt, moves_list):
        att = vm.head_attention(model, tok, tt, *vm.HEAD).cpu().numpy()
        acc = {k: [] for k in ("bos", "self", "last_mover_any", "last_mover_same_col", "other_player_any", "last_mover_prev1", "last_mover_prev2")}
        for k, mv in enumerate(moves_list):
            t = len(mv); c = mv[-1]
            keys = np.arange(1, t)                            # earlier moves: key s = move s-1
            same_player = ((keys - 1) % 2) == ((t - 1) % 2)
            same_col = np.array([mv[s - 1] == c for s in keys], dtype=bool)
            a = att[k, 1:t]
            acc["bos"].append(att[k, 0]); acc["self"].append(att[k, t])
            acc["last_mover_any"].append(a[same_player].sum()); acc["other_player_any"].append(a[~same_player].sum())
            acc["last_mover_same_col"].append(a[same_player & same_col].sum())
            lm = np.flatnonzero(same_player)[::-1]             # last mover's earlier moves, most recent first
            acc["last_mover_prev1"].append(a[lm[0]] if len(lm) > 0 else 0.0)
            acc["last_mover_prev2"].append(a[lm[1]] if len(lm) > 1 else 0.0)
        return {k: float(np.mean(v)) for k, v in acc.items()}
    Pv = V.P
    out["attention_vertical_pairs"] = breakdown(V.tok["clean"], V.t, [Pv["clean"][k][: Pv["t"][k]].tolist() for k in range(V.N)])
    mv, sc, ln = data["val"]
    rng = np.random.default_rng(SEED)
    g = rng.choice(len(ln), 600, replace=False)
    seqs = [mv[i, :t].tolist() for i in g for t in range(4, int(ln[i]))][:4000]
    toks = torch.stack([tokens_from_moves(torch.as_tensor(np.array([s + [-1] * (42 - len(s))], dtype=np.int8)))[0] for s in seqs]).to(DEV)
    out["attention_all_positions"] = breakdown(toks, torch.as_tensor([len(s) for s in seqs], device=DEV), seqs)
    # (b) first direction of each layer vs binary facts
    U = {}
    for l in range(5):
        X = (D.acts["clean"][:, l] - D.acts["corr"][:, l]).float()
        U[l] = torch.linalg.svd(X, full_matrices=False)[2][0]
    bs = ns.BoardSet(mv, ln)
    el = ns.eligible(ln, 4)
    run = vm.opp_run_on_last_col(bs)
    _, _, block, _ = C.facts(bs.pos, bs.mask)
    rows = np.arange(len(bs.t)); lc = np.maximum(bs.last_col.astype(np.int64), 0)
    facts = {"vertical threat on the last-move column (run 3, cell above empty)": run >= 3,
             "opponent run >= 2 on the last-move column": run >= 2,
             "any must-block": block.any(1),
             "must-block in the last-move column": block[rows, lc]}
    proj = {l: [] for l in range(5)}
    with torch.no_grad():
        for i in range(0, len(ln), 512):
            tok = tokens_from_moves(torch.as_tensor(mv[i:i + 512])).to(DEV)
            valid = torch.arange(42, device=DEV)[None] < torch.as_tensor(ln[i:i + 512], device=DEV)[:, None]

            def hook(l, a, g_, u):
                if l < 5:
                    proj[l].append((a[:, :42][valid] @ U[l]).cpu())
                return a
            model(tok, hook=hook)
    au = {}
    for l in range(5):
        p = torch.cat(proj[l]).numpy()
        au[str(l)] = {k: float(max(roc_auc_score(v[el], p[el]), 1 - roc_auc_score(v[el], p[el]))) for k, v in facts.items()}
    out["direction_auroc"] = au
    out["fact_base_rates"] = {k: float(v[el].mean()) for k, v in facts.items()}
    path = config.ROOT / "results" / "vertical_posthoc.json"
    path.write_text(json.dumps(out, indent=1))
    provenance.write(path, {"posthoc": True})
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
