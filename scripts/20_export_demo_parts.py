"""Parts of the model the demo can switch off (tactic-specific heads, an MLP layer, the top neurons per tactic), with the mean
activations that mean-ablation needs, plus PyTorch reference outputs under each ablation to check the JavaScript port.
Writes web/parts.json, web/reference_parts.json. Needs results/tactic_atlas.json."""
import json

import numpy as np
import torch

from c4n import config, provenance
from c4n import tactics as T
from c4n.data import load_split
from c4n.model import load_checkpoint, tokens_from_moves

CFG = config.load()
AC = CFG["analysis"]
DEV = "cuda" if torch.cuda.is_available() else "cpu"
WEB = config.ROOT / "web"


def main():
    model = load_checkpoint(config.ROOT / AC["checkpoint"], DEV)
    moves, _, lengths = load_split(CFG, "analysis")
    n = AC["n_games"]
    mean_a, mean_y = T.means(model, moves[:n], lengths[:n], DEV)
    atlas = json.loads((config.results_dir(CFG) / "tactic_atlas.json").read_text())
    parts = [
        {"id": "L0H3", "label": "Layer 0, attention head 3", "why": "carries blocking: removing it costs the model most of its blocking", "heads": [[0, 3]], "mlp": [], "neurons": []},
        {"id": "L0H5", "label": "Layer 0, attention head 5", "why": "carries taking a win", "heads": [[0, 5]], "mlp": [], "neurons": []},
        {"id": "L5H34", "label": "Layer 5, attention heads 3 and 4", "why": "help with making forks", "heads": [[5, 3], [5, 4]], "mlp": [], "neurons": []},
        {"id": "L5MLP", "label": "Layer 5 MLP (all 1,024 neurons)", "why": "the output layer's MLP: matters for blocking and forks, and for the model in general", "heads": [], "mlp": [5], "neurons": []},
    ]
    names = {"win": "taking a win", "block": "blocking", "poison": "avoiding a poisoned column", "fork": "making a fork"}
    for t in T.TACTICS:
        parts.append({"id": f"top_{t}", "label": f"The 50 neurons that most support {names[t]}", "why": "ranked by first-order effect on the tactic; the rest of the model stays intact",
                      "heads": [], "mlp": [], "neurons": [[x["layer"], x["neuron"]] for x in atlas["top_neurons"][t][:50]]})
    # example positions where switching a part off makes the model fail a tactic it normally gets right
    sets = T.tactic_sets(moves[:n], lengths[:n], 3000, CFG["seed"])
    focus = {"L0H3": "block", "L0H5": "win", "L5H34": "fork", "L5MLP": "block", "top_fork": "fork", "top_block": "block"}

    def hooks_for(p, model_):
        h = {}
        if p["mlp"]:
            h["hook"] = lambda l, a, g, u, ls=p["mlp"]: (mean_a[l].to(a.device).expand_as(a).clone() if l in ls else a)
        if p["neurons"]:
            h["hook"] = T.neuron_zero_hook({l: [nn for ll, nn in p["neurons"] if ll == l] for l in range(model_.cfg["n_layer"])})
        if p["heads"]:
            hs = {(l, hh) for l, hh in p["heads"]}

            def ah(l, y, hs=hs):
                y = y.clone()
                for (ll, hh) in hs:
                    if ll == l:
                        y[:, hh] = mean_y[l, hh].to(y.device)[None, None, :]
                return y
            h["attn_hook"] = ah
        return h

    examples = []
    for p in parts:
        t = focus.get(p["id"])
        if t is None:
            continue
        gt = sets[t]
        p_i, ok_i = T.good_prob(model, moves, gt, DEV)
        p_a, ok_a = T.good_prob(model, moves, gt, DEV, **hooks_for(p, model))
        tt = gt["_t"][gt["idx"]]
        cand = np.flatnonzero(ok_i & ~ok_a & (p_i > 0.9) & (p_a < 0.3) & (tt >= 6))
        cand = cand[np.argsort(tt[cand])][:2]  # shortest games first: clearer boards
        for c in cand:
            g = int(gt["_g"][gt["idx"][c]]); tp = int(tt[c])
            examples.append({"part": p["id"], "tactic": t, "moves": "".join(str(int(x)) for x in moves[g, :tp]), "t": tp, "good": np.flatnonzero(gt["good"][c]).tolist(),
                             "p_intact": round(float(p_i[c]), 3), "p_ablated": round(float(p_a[c]), 3)})
    print(len(examples), "example positions")
    out = {"parts": parts, "examples": examples, "mean_a": np.round(mean_a.numpy(), 5).tolist(), "mean_y": np.round(mean_y.numpy(), 5).tolist()}
    (WEB / "parts.json").write_text(json.dumps(out, separators=(",", ":")))
    import copy
    mr = copy.deepcopy(model).half().float()  # the shipped weights are float16: the reference must use the same rounded weights
    ref = {}
    for p in parts:
        hooks = {}
        if p["mlp"]:
            hooks["hook"] = lambda l, a, g, u, ls=p["mlp"]: (mean_a[l].to(a.device).expand_as(a).clone() if l in ls else a)
        if p["neurons"]:
            hooks["hook"] = T.neuron_zero_hook({l: [nn for ll, nn in p["neurons"] if ll == l] for l in range(model.cfg["n_layer"])})
        if p["heads"]:
            hs = {(l, h) for l, h in p["heads"]}

            def ah(l, y, hs=hs):
                y = y.clone()
                for (ll, h) in hs:
                    if ll == l:
                        y[:, h] = mean_y[l, h].to(y.device)[None, None, :]
                return y
            hooks["attn_hook"] = ah
        rows = []
        for gi in range(3):
            tok = tokens_from_moves(torch.as_tensor(moves[gi:gi + 1]))[:, : int(lengths[gi]) + 1]
            with torch.no_grad():
                lg = mr(tok.to(DEV), **hooks)
            rows.append({"tokens": tok[0].tolist(), "logits": lg[0].float().cpu().tolist()})
        ref[p["id"]] = rows
    (WEB / "reference_parts.json").write_text(json.dumps(ref))
    provenance.write(WEB / "parts.json", CFG)
    print(len(parts), "parts")


if __name__ == "__main__":
    main()
