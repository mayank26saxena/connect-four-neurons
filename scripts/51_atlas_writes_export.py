"""What each neuron pole writes, for the neuron atlas (PLAN addendum (v), V1-V2): docs/blog/neuron-atlas/data/writes.js.
Per pole (pid order, 12,288): the J-lens column readout for a strong firing (p99 activation, centred logits), the top five readable
concepts of the concept readout with their values (z units), and, where measured, the column and concept whose value fell most
when the pole was switched off on held-out games. From results/outputs_readouts.npz; light array work, no model is run."""
import json

import numpy as np

from c4n import config
from c4n.concepts import NAMES

ROOT = config.ROOT
R = np.load(ROOT / "results" / "outputs_readouts.npz")
CFG = config.load("outputs")
OUT = ROOT / "docs" / "blog" / "neuron-atlas" / "data" / "writes.js"


def main():
    used, size, readJ = R["used"], R["size"], R["readJ"]
    rd = np.flatnonzero(R["readable"])
    rc = R["readC"].astype(np.float32)[:, rd] * size[:, None]
    dcol, dcon = R["dcol"], R["dcon"].astype(np.float32)[:, rd]
    top = np.argsort(-rc, 1)[:, :5]
    J, C, CV, CC, CK = [], [], [], [], []
    for p in range(len(used)):
        if not used[p]:
            J.append(None); C.append(None); CV.append(None); CC.append(-1); CK.append(-1); continue
        J.append([round(float(v), 3) for v in readJ[p] * size[p]])
        C.append([int(i) for i in top[p]]); CV.append([round(float(rc[p, i]), 2) for i in top[p]])
        CC.append(int(dcol[p].argmax()) if dcol[p].max() >= CFG["col_measurable"] else -1)
        CK.append(int(dcon[p].argmax()) if dcon[p].max() >= CFG["concept_measurable"] else -1)
    d = {"names": [NAMES[i] for i in rd], "J": J, "C": C, "CV": CV, "causal_col": CC, "causal_concept": CK}
    OUT.write_text("window.WRITES = " + json.dumps(d, separators=(",", ":")) + ";\n")
    print(f"wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB), {int(used.sum())} used poles")


if __name__ == "__main__":
    main()
