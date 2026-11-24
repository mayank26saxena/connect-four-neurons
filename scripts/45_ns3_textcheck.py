"""Test B text-only check (PLAN.md addendum (s), S7, prediction s-B2). A fresh model, blind to group, reads each English description
and its effect line and answers one question per unit. Built from ns3/descriptions/ only (no answer key is read by `export`).

  export   write ns3/textcheck/pack.json (items in a seeded random order under new ids T01-T50) and ns3/textcheck/PROMPT.md;
           the id map back to units goes to ns3/textcheck/map.json (not needed by the judge; keep it out of the judge's folder)
  score    read ns3/textcheck/answers.json ({"T01": "yes", ...}), map back to units and write ns3/textcheck/scored.json

The judge runs on a separate Claude account (LLM jobs go there). Give it only pack.json and PROMPT.md."""
import argparse
import json
import random

from c4n import config

ROOT = config.ROOT
NS3 = ROOT / "ns3"
OUT = NS3 / "textcheck"
SEED = 20261124
QUESTION = "Does this describe the opponent threatening to win, or blocking it?"

PROMPT = """# Text-only check

You will read 50 short descriptions of units inside a small neural network that plays Connect Four. Each item has a
`description` (when the unit is active) and an `effect` (what it does to the model's move when it is pushed up or down).

For each item, answer one question with "yes" or "no":

> {q}

Answer "yes" if the description and effect, read together, are about the opponent having (or being about to have) a way
to win, or about the player to move blocking that, even if they also mention other things. Answer "no" otherwise. Judge
only the text. Do not run code and do not look for other files.

Write `answers.json` as a single JSON object mapping each item id to "yes" or "no", for example
{{"T01": "no", "T02": "yes", ...}}, with all 50 ids. Then add `reasons.json` with one short sentence per id.
"""


def cmd_export(_):
    units = sorted(p.stem for p in (NS3 / "descriptions").glob("U*.json"))
    items = []
    for u in units:
        d = json.loads((NS3 / "descriptions" / f"{u}.json").read_text())
        items.append({"unit": u, "description": d["description"], "effect": d.get("effect", "")})
    random.Random(SEED).shuffle(items)
    OUT.mkdir(exist_ok=True)
    pack, idmap = [], {}
    for i, it in enumerate(items, 1):
        t = f"T{i:02d}"
        idmap[t] = it["unit"]
        pack.append({"id": t, "description": it["description"], "effect": it["effect"]})
    (OUT / "pack.json").write_text(json.dumps({"question": QUESTION, "items": pack}, indent=1))
    (OUT / "PROMPT.md").write_text(PROMPT.format(q=QUESTION))
    (OUT / "map.json").write_text(json.dumps(idmap, indent=1))
    print(f"wrote {len(pack)} items to {OUT}/pack.json (seed {SEED})")


def cmd_score(_):
    idmap = json.loads((OUT / "map.json").read_text())
    ans = json.loads((OUT / "answers.json").read_text())
    missing = sorted(set(idmap) - set(ans))
    if missing:
        raise SystemExit(f"answers missing for {missing}")
    per = {idmap[t]: str(a).strip().lower() == "yes" for t, a in ans.items()}
    (OUT / "scored.json").write_text(json.dumps({"question": QUESTION, "yes": per}, indent=1))
    print(f"{sum(per.values())} of {len(per)} answered yes")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("export"); sp.add_parser("score")
    a = p.parse_args()
    {"export": cmd_export, "score": cmd_score}[a.cmd](a)


if __name__ == "__main__":
    main()
