"""Per-neuron data for the live neuron map in the blog post (docs/blog/post/data/atlas.js).
For each of the 6 x 1,024 neurons: its best-matching concept (pole with the higher held-out F1 in the existing atlas data), the firing
thresholds of both poles (to scale live activations), and its roles: member of the vertical-block circuit (results/vertical_map.json),
column alarm (with the column it promotes), member of the 200 most important blocking neurons (results/block_circuit.json), and the
agent's description if (q)/(r) described it. Neurons in each layer are ordered by concept family, then F1, so families form regions.
Light JSON work; no model is run."""
import json

from c4n import config
from c4n.concepts import FAMILY, NAMES

ROOT = config.ROOT
ATL = ROOT / "docs" / "blog" / "atlas" / "data"
OUT = ROOT / "docs" / "blog" / "post" / "data" / "atlas.js"
FAM_ORDER = ["block_now", "win_now", "my_threat", "opp_threat", "poison", "line", "land", "cell", "full", "last", "ply", "eval", "other"]


def fam_of(name):
    f = FAMILY[NAMES.index(name)]
    for k in FAM_ORDER:
        if f.startswith(k):
            return k
    return "other"


def main():
    vm = json.loads((ROOT / "results" / "vertical_map.json").read_text())
    bc = json.loads((ROOT / "results" / "block_circuit.json").read_text())
    V = {(n["layer"], n["neuron"]): n["pole"] for n in vm["circuit"]["neurons"]}
    Rcol = {a["id"] % 1024: a["promotes"] for a in vm["u3_alarms"]["neurons"]}
    C200 = {(n["layer"], n["neuron"]) for n in bc["circuit"]["neurons"]}
    desc = {}
    for study, ws in (("q", "ns"), ("r", "ns2")):
        for r in json.loads((ROOT / ws / "report.json").read_text())["rows"]:
            if r["kind"] == "neuron":
                d = json.loads((ROOT / ws / "descriptions" / f"{r['unit']}.json").read_text())
                desc.setdefault((r["layer"], r["neuron"]), []).append({"id": f"{study}-{r['unit']}", "pole": r["pole"], "f1": round(r["test_f1"], 2), "text": d["description"]})
    # (s) Test B, the blind run after the circuit was frozen: circuit poles and decoys (random directions are not neurons)
    for r in json.loads((ROOT / "results" / "ns3_testB.json").read_text())["rows"]:
        if r["neuron"] is not None:
            desc.setdefault((r["layer"], r["neuron"]), []).append({"id": f"s-{r['unit']}", "pole": r["pole"], "f1": round(r["f1_p97"], 2), "text": r["description"],
                                                                   "group": r["group"], "ta": round(r["tactic_agreement"], 2)})
    fams_seen, neurons, orders = set(), [], []
    for l in range(6):
        L = json.loads((ATL / f"L{l}.json").read_text())
        rows = []
        for x in L:
            best = max(x["poles"], key=lambda p: p["F1"][0])
            cname, f1 = NAMES[best["C"][0]], best["F1"][0]
            fam = fam_of(cname) if f1 >= 0.3 else "none"
            fams_seen.add(fam)
            thr = {p["s"]: p["thr"] for p in x["poles"]}
            k = (l, x["n"])
            rows.append({"l": l, "n": x["n"], "c": cname if f1 >= 0.3 else None, "f1": round(f1, 2), "pole": best["s"], "fam": fam,
                         "tp": thr.get("+"), "tn": thr.get("-"), "v": k in V, "vp": V.get(k), "a": Rcol.get(x["n"]) if l == 5 and k in V else None,
                         "b": k in C200, "ds": desc.get(k, []),
                         # "d": the description shown on the post's map: the circuit pole's if described, else the best-scoring one
                         "d": next((x for x in desc.get(k, []) if x["pole"] == V.get(k)), max(desc.get(k, []), key=lambda x: x["f1"], default=None))})
        fo = FAM_ORDER + ["none"]
        order = sorted(range(len(rows)), key=lambda i: (fo.index(rows[i]["fam"]), -rows[i]["f1"]))
        orders.append([rows[i]["n"] for i in order])
        neurons += rows
    counts = {"described_in_circuit_same_pole": sum(bool(r["d"]) and r["v"] and r["d"]["pole"] == r["vp"] for r in neurons),
              "vertical": sum(r["v"] for r in neurons), "alarms": sum(r["a"] is not None for r in neurons),
              "block200": sum(r["b"] for r in neurons), "described": sum(len(r["ds"]) for r in neurons)}
    assert counts["vertical"] == vm["circuit"]["size"] and counts["alarms"] == len(vm["u3_alarms"]["neurons"]), counts
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("window.ATLAS = " + json.dumps({"families": [f for f in FAM_ORDER + ["none"] if f in fams_seen], "order": orders,
                                                    "neurons": neurons, "counts": counts}, separators=(",", ":")) + ";\n")
    print(f"{len(neurons)} neurons; {counts}; {OUT.stat().st_size / 1e3:.0f} kB")


if __name__ == "__main__":
    main()
