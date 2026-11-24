"""Score the validity tests T1-T7 (docs/PLAN.md addendum e) with the decision rules written there. Stdlib only.

Reads results/ (main model), results/sweep/<run>/, results/robust/<run>/. Writes results/validity_summary.json and prints
a table. A test whose inputs are missing is reported as "incomplete", never as passed.
"""
import json
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"


def load(d, name):
    p = d / name
    return json.loads(p.read_text()) if p.exists() else None


def dirs():
    out = {"main": RES}
    for sub in ("sweep", "robust"):
        if (RES / sub).exists():
            out.update({f"{sub}/{p.name}": p for p in sorted((RES / sub).iterdir()) if p.is_dir()})
    return out


def gap(d):
    c = load(d, "concepts_summary.json")
    return None if c is None else c["neurons"]["f1_sweep"]["share_ge_0.5"] - c["random_rotation"]["f1_sweep"]["share_ge_0.5"]


def top_mode(d):
    m = load(d, "modes.json")
    return None if m is None else m["summary_random_sample"]["share_top_mode_ge_0.9"]


def d_ff(d):
    b = load(d, "basis_controls.json")
    return None if b is None else b["d_ff"]


R = {k: {"gap": gap(d), "top_mode": top_mode(d), "basis": load(d, "basis_controls.json"), "crossfit": load(d, "crossfit.json")} for k, d in dirs().items()}
out = {"runs": {}, "tests": {}}
rows = []
for k, r in R.items():
    row = {"run": k}
    b = r["basis"]
    if b:
        c = b["conditions"]
        intact = c["intact"]["agree"]
        band = c["band_P5-P95"]
        row.update(d_ff=b["d_ff"], kurt_neuron=b["kurtosis_mean"]["neuron"], kurt_rotation=b["kurtosis_mean"]["rotation"],
                   top5_neuron=b["top5_energy"]["neuron"], top5_rotation=b["top5_energy"]["rotation"],
                   cost_neuron=intact - band["neuron"]["agree"], cost_rotation=intact - st.mean(x["agree"] for x in band["rotation"]))
    x = r["crossfit"]
    if x:
        row.update(cf_diff=x["diff_heldout"]["mean"], cf_ci=x["diff_heldout"]["ci95"], cf_neuron=x["neuron"]["share_heldout"], cf_rotation=x["rotation"]["share_heldout"],
                   cf_local={f: [x["neuron"]["families_heldout"].get(f, 0), x["rotation"]["families_heldout"].get(f, 0)] for f in ("line", "land", "cell")})
    row.update(gap=r["gap"], top_mode=r["top_mode"])
    out["runs"][k] = row
    rows.append(row)

T = out["tests"]
b_rows = [r for r in rows if "kurt_neuron" in r]
T["T1"] = ({"status": "incomplete"} if not b_rows else {"holds": all(r["kurt_neuron"] > r["kurt_rotation"] for r in b_rows), "n_models": len(b_rows),
           "kurtosis_neuron_range": [min(r["kurt_neuron"] for r in b_rows), max(r["kurt_neuron"] for r in b_rows)],
           "kurtosis_rotation_range": [min(r["kurt_rotation"] for r in b_rows), max(r["kurt_rotation"] for r in b_rows)]})
T["T2"] = ({"status": "incomplete"} if not b_rows else {"holds": all(r["cost_rotation"] > r["cost_neuron"] for r in b_rows), "n_models": len(b_rows),
           "cost_neuron_range": [min(r["cost_neuron"] for r in b_rows), max(r["cost_neuron"] for r in b_rows)],
           "cost_rotation_range": [min(r["cost_rotation"] for r in b_rows), max(r["cost_rotation"] for r in b_rows)]})
cf = [r for r in rows if "cf_diff" in r]
wide = [r for r in cf if r.get("d_ff", 0) >= 1024]
T["T3"] = ({"status": "incomplete"} if not wide else {"holds_aggregate": all(r["cf_ci"][1] < 0 for r in wide), "n_models_ge_1024": len(wide),
           "holds_local": all(all(r["cf_local"][f][0] > r["cf_local"][f][1] for f in ("line", "land", "cell")) for r in wide)})
seeds = {}
for k, r in R.items():
    if k.startswith("sweep/w") and r["gap"] is not None:
        w, s = k.split("/w")[1].split("_s")
        seeds.setdefault(int(w), {})[int(s)] = r["gap"]
common = sorted(set(seeds.get(256, {})) & set(seeds.get(4096, {})))
T["T4"] = ({"status": "incomplete"} if not common else {"holds": all(seeds[256][s] > seeds[4096][s] for s in common), "paired_seeds": common,
           "gap_by_width_mean_sd": {w: [st.mean(v.values()), st.pstdev(v.values()) if len(v) > 1 else None, len(v)] for w, v in sorted(seeds.items())}})
ref = R.get("sweep/w1024_s1", {})


def vs_ref(name):
    r = R.get(f"robust/{name}")
    return None if not r or r["gap"] is None or ref.get("gap") is None else r


r5 = vs_ref("len32k")
T["T5"] = {"status": "incomplete"} if not r5 else {"holds": abs(r5["gap"] - ref["gap"]) < 0.02 and abs(r5["top_mode"] - ref["top_mode"]) < 0.05,
                                                    "gap_change": r5["gap"] - ref["gap"], "top_mode_change": r5["top_mode"] - ref["top_mode"]}
w = {n: vs_ref(n) for n in ("wd0", "wd1")}
T["T6"] = {"status": "incomplete"} if not all(w.values()) else {"depends_on_weight_decay": any(abs(v["gap"] - ref["gap"]) > 0.03 for v in w.values()),
                                                                 "gap_change": {n: v["gap"] - ref["gap"] for n, v in w.items()}}
a, c = vs_ref("dm512_ff1024"), vs_ref("dm512_ff2048")
T["T7"] = {"status": "incomplete"} if not (a and c) else {"holds": a["gap"] > ref["gap"] and abs(c["gap"] - ref["gap"]) < 0.02,
                                                           "gap": {"d256_ff1024_ratio4": ref["gap"], "d512_ff1024_ratio2": a["gap"], "d512_ff2048_ratio4": c["gap"]}}
(RES / "validity_summary.json").write_text(json.dumps(out, indent=1))
for k, v in T.items():
    print(k, json.dumps(v))
print(f"{len(rows)} models; with basis controls {len(b_rows)}, with cross-fit {len(cf)}")
