"""Data for the vertical-blocker demo (docs/blog/vertical/) from tracked result files only (PLAN addendum u).
Reads web/vertical.json, results/vertical_map.json, results/orientation_followup.json, results/block_circuit.json and the (q)/(r)
reports (for which layer-5 alarm neurons an agent described). Writes docs/blog/vertical/data/vertical.js (window.VDATA) and copies
web/c4model.js next to the page. Checks: the demo's switch numbers equal the result file's, and the page's model weights are the
analysed ones. Light JSON work; no model is run."""
import hashlib
import json
import shutil

from c4n import config

ROOT = config.ROOT
PAGE = ROOT / "docs" / "blog" / "vertical"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    demo = json.loads((ROOT / "web" / "vertical.json").read_text())
    vm = json.loads((ROOT / "results" / "vertical_map.json").read_text())
    of = json.loads((ROOT / "results" / "orientation_followup.json").read_text())["layers0-4"]
    bc = json.loads((ROOT / "results" / "block_circuit.json").read_text())
    ph = json.loads((ROOT / "results" / "vertical_posthoc.json").read_text())  # post-hoc, descriptive (scripts/40b)
    assert not vm["smoke"], "use the full run"
    assert demo["switch_accuracy"] == vm["u5_switches"]["accuracy"], "demo and result file disagree on switch accuracy"
    assert demo["readout_size"] == len(vm["u3_alarms"]["neurons"])
    assert sha(ROOT / "docs" / "blog" / "demo" / "model.bin") == sha(ROOT / "web" / "model.bin"), "page weights differ"
    s_vertical = bc["faithfulness"]["s6_circuit_size_by_orientation"]["vertical"]["size"]
    described = {}
    for study, ws in (("q", "ns"), ("r", "ns2")):
        for r in json.loads((ROOT / ws / "report.json").read_text())["rows"]:
            if r["kind"] == "neuron" and r["layer"] == 5:
                d = json.loads((ROOT / ws / "descriptions" / f"{r['unit']}.json").read_text())
                described[(r["neuron"], r["pole"])] = {"id": f"{study}-{r['unit']}", "description": d["description"], "test_f1": r["test_f1"]}
    alarm_desc = [{"neuron": a["neuron"], "pole": a["pole"], "promotes": a["promotes"], **described[(a["neuron"], a["pole"])]}
                  for a in vm["u3_alarms"]["neurons"] if (a["neuron"], a["pole"]) in described]
    m = {"u1": vm["u1_attention"], "u2": vm["u2_readout_moved"], "u3": {"share": vm["u3_alarms"]["share_promote_equals_best_col"],
         "holds": vm["u3_alarms"]["holds"]}, "u4": vm["u4_direction_meaning"],
         "u5": {"i": vm["u5_switches"]["i_holds"], "ii": vm["u5_switches"]["ii_holds"], "iii": vm["u5_switches"]["iii_holds"]},
         "circuit": {"size": vm["circuit"]["size"], "by_layer": vm["circuit"]["by_layer"], "s_size": s_vertical,
                     "confirm_effect": vm["circuit"]["confirm_effect"]},
         "readout_confirm_effect": vm["readout_confirm_effect"], "directions_confirm_effect": vm["directions_confirm_effect"],
         "alarm_descriptions": alarm_desc,
         "posthoc": {"attention": ph["attention_vertical_pairs"], "attention_all": ph["attention_all_positions"],
                     "auroc_threat": {l: v["vertical threat on the last-move column (run 3, cell above empty)"] for l, v in ph["direction_auroc"].items()},
                     "threat_base_rate": ph["fact_base_rates"]["vertical threat on the last-move column (run 3, cell above empty)"]}}
    orient = {o: {"n80": of[o]["T1"]["n80"], "d80": of[o]["T2"]["d80"], "d80_confirm": of[o]["T2"].get("confirm_effect"),
                  "top_head_effect": of[o]["T3"]["top_effect"]} for o in ("vertical", "horizontal", "diagonal")}
    (PAGE / "data").mkdir(parents=True, exist_ok=True)
    (PAGE / "data" / "vertical.js").write_text("window.VDATA = " + json.dumps({"demo": demo, "map": m, "orient": orient}) + ";\n")
    shutil.copy2(ROOT / "web" / "c4model.js", PAGE / "c4model.js")
    assert sha(PAGE / "c4model.js") == sha(ROOT / "web" / "c4model.js")
    print(f"vertical circuit {m['circuit']['size']} neurons (s: {s_vertical}); {demo['readout_size']} layer-5 alarms, "
          f"{len(alarm_desc)} described in (q)/(r); wrote {PAGE / 'data' / 'vertical.js'}")


if __name__ == "__main__":
    main()
