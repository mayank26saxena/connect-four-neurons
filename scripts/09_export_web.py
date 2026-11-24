"""Export the analysed checkpoint for the in-browser demo, plus reference outputs for checking the JS port.

Writes web/model.json + web/model.bin (float16 weights), web/reference.json (logits and activations from PyTorch on
analysis games, computed from the float16-rounded weights so the comparison isolates the JS arithmetic), and
web/poles.json (the concept-matched pole catalog the demo labels neurons with).
"""
import json

import numpy as np
import torch

from c4n import config, provenance
from c4n.data import load_split
from c4n.model import load_checkpoint, tokens_from_moves

CFG = config.load()
AC = CFG["analysis"]
WEB = config.ROOT / "web"


def main():
    model = load_checkpoint(config.ROOT / AC["checkpoint"], "cpu")
    sd = model.state_dict()
    man = {"config": model.cfg, "weights": "model.bin", "dtype": "float16", "tensors": {}}
    blob, off = bytearray(), 0
    for k, v in sd.items():
        a = v.detach().numpy().astype(np.float16)
        man["tensors"][k] = {"shape": list(a.shape), "offset": off}
        blob += a.tobytes(); off += a.nbytes
        sd[k] = torch.from_numpy(a.astype(np.float32))
    (WEB / "model.bin").write_bytes(bytes(blob))
    (WEB / "model.json").write_text(json.dumps(man))
    model.load_state_dict(sd)  # float16-rounded weights for the reference outputs
    moves, _, lengths = load_split(CFG, "analysis")
    ref = []
    for gi in range(5):
        n = int(lengths[gi])
        tok = tokens_from_moves(torch.as_tensor(moves[gi:gi + 1]))[:, :n + 1]
        store = {}
        model(tok, hook=lambda l, a, g, u: store.__setitem__(l, a) or a)
        lg = model(tok)
        ref.append({"tokens": tok[0].tolist(), "logits": lg[0].tolist(),
                    "acts_layer3_last": store[3][0, -1].tolist()})
    (WEB / "reference.json").write_text(json.dumps(ref))
    rows = json.loads((config.results_dir(CFG) / "pole_table.json").read_text())
    keep = [r for r in rows if r["f1_sweep"] >= CFG["web"]["min_f1"]]
    # force-on value per pole: its p99.5 (positive pole) or p0.5 (negative pole) over the analysis split
    from c4n import analysis as A
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(dev)
    acts, _, _ = A.collect(model, moves[:CFG["analysis"]["n_games"]], lengths[:CFG["analysis"]["n_games"]], dev)
    chi, clo = A.percentiles(acts, [99.5, 0.5], dev)
    model.to("cpu")
    for r in keep:
        r["clamp"] = round(float((chi if r["pole"] == "+" else clo)[r["layer"], r["neuron"]]), 4)
    (WEB / "poles.json").write_text(json.dumps(keep))
    ga = config.results_dir(CFG) / "group_action.json"
    if ga.exists():
        groups = {c["concept"]: c["top_poles"][:CFG["web"]["group_size"]] for c in json.loads(ga.read_text())["concepts"]}
        (WEB / "groups.json").write_text(json.dumps(groups))
    for p in ("model.bin", "poles.json"):
        provenance.write(WEB / p, CFG)
    print(f"weights {off / 1e6:.1f} MB, {len(keep)} labelled poles")


if __name__ == "__main__":
    main()
