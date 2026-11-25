"""Follow-up to (v) V3, labelled, not registered (decided after seeing that most registered type-3 pairs are two concepts about the
same cell or column, e.g. cell_r5c0_mine and cell_r5c0_theirs, which have |phi| < 0.1 because they are mutually exclusive and rare).
Same pole set, same "adds" rule; two concepts now count as related if |phi| >= 0.1 OR they name the same column. Reports the share
of measurable poles that add two concepts about different columns that are also uncorrelated, with examples.
Needs results/outputs_readouts.npz. Writes results/outputs_v3_followup.json. GPU host (dev concept labels are cached there)."""
import json
import re

import numpy as np
import torch

from c4n import config
from c4n import outputs as O
from c4n.concepts import NAMES
from c4n.data import concepts_for
from c4n.tactics import position_index
from c4n import ns

CFG = config.load("outputs")
RES = config.results_dir(CFG)
DEV = "cuda" if torch.cuda.is_available() else "cpu"


def col(name):
    m = re.search(r"c(\d)(?:_|$)", name)
    return int(m.group(1)) if m else None


def main():
    R = np.load(RES / "outputs_readouts.npz")
    _, _, dln = ns.load_games("analysis", CFG["n_games"])
    _, dt = position_index(dln)
    Yd = concepts_for({"data": CFG["data"]}, "analysis", CFG["n_games"])[dt >= CFG["min_ply"]]
    PHI = np.abs(np.nan_to_num(O.phi(Yd, DEV).numpy()))
    rd = np.flatnonzero(R["readable"]); cc = R["dcon"].astype(np.float32)[:, rd]
    cols = [col(NAMES[i]) for i in rd]
    meas = R["used"] & (cc.max(1) >= CFG["concept_measurable"])
    reg, fol, ex = 0, 0, []
    Fd = 1024
    for p in np.flatnonzero(meas):
        mx = cc[p].max()
        a = np.flatnonzero((cc[p] >= CFG["concept_measurable"]) & (cc[p] >= CFG["adds_frac"] * mx))
        r3 = f3 = False
        pair = None
        for i in range(len(a)):
            for j in range(i + 1, len(a)):
                u = PHI[rd[a[i]], rd[a[j]]] < CFG["unrelated_phi"]
                r3 |= u
                if u and not (cols[a[i]] is not None and cols[a[i]] == cols[a[j]]):
                    f3 = True; pair = pair or (NAMES[rd[a[i]]], NAMES[rd[a[j]]])
        reg += r3; fol += f3
        if f3 and len(ex) < 12:
            l, n, s = O.unpid(int(p), Fd)
            ex.append({"layer": int(l), "neuron": int(n), "pole": "+" if s > 0 else "-", "pair": pair})
    out = {"label": "follow-up, not registered", "measurable": int(meas.sum()), "type3_registered_rule": int(reg),
           "type3_registered_share": reg / max(1, meas.sum()), "type3_followup": int(fol), "type3_followup_share": fol / max(1, meas.sum()),
           "examples": ex}
    (RES / "outputs_v3_followup.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
