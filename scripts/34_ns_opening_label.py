"""Post-hoc label for the atlas (follow-up to studies q and r, not part of either pre-registration): is a unit an "opening unit"?

Every game starts from the same few positions, which made exact one-line rules possible in study (q) (addendum r). For each unit with
held-out F1 >= 0.5, run its frozen program (sandboxed, c4n.ns.load_program) on the first 1,000 validation games and record the
share of positions where it predicts firing that have fewer than 4 stones. A unit is labelled an opening unit if that share is
>= 0.5. Scores are not changed. Writes ns/opening_label.json."""
import json

import numpy as np

from c4n import config, ns

ROOT = config.ROOT


def main():
    moves, _, lengths = ns.load_games(ns.TEST_SPLIT, 1000)
    bs = ns.BoardSet(moves, lengths)
    early = bs.t < 4
    out = {"rule": "share of predicted-firing positions with fewer than 4 stones >= 0.5 (first 1,000 validation games)", "units": {}}
    for study, ws in (("q", "ns"), ("r", "ns2")):
        for r in json.loads((ROOT / ws / "report.json").read_text())["rows"]:
            if r["test_f1"] < 0.5:
                continue
            prog = json.loads((ROOT / ws / "descriptions" / f"{r['unit']}.json").read_text())["program"]
            fires, _ = ns.load_program(prog)
            pred = ns.run_program(fires, bs) >= 0.5
            share = float(early[pred].mean()) if pred.any() else float("nan")
            out["units"][f"{study}-{r['unit']}"] = {"early_share": round(share, 3), "opening": bool(share >= 0.5), "n_pred": int(pred.sum())}
    (ROOT / "ns" / "opening_label.json").write_text(json.dumps(out, indent=1))
    lab = [k for k, v in out["units"].items() if v["opening"]]
    print(len(out["units"]), "units checked;", len(lab), "opening units:", lab)


if __name__ == "__main__":
    main()
