"""Build the blog post draft docs/blog/post/ (PLAN addenda h-u) from tracked result files only.
Every number in the text is a {{key|fmt}} placeholder filled here; figures go to docs/blog/post/data/figures.js. Checks recompute
headline numbers from the raw result files (ladder correlation, totals, the frozen circuit hash) and fail on mismatch. Light JSON work."""
import hashlib
import json
import re
import statistics as st

import numpy as np

from c4n import config

ROOT = config.ROOT
R = ROOT / "results"
OUT = ROOT / "docs" / "blog" / "post"
J = lambda name: json.loads((R / name).read_text())
V = {}


def put(k, v, fmt="s"):
    assert k not in V, k
    V[k] = (v, fmt)


def main():
    cfg = config.load()
    tr = J("train_curve_main.json"); play = J("play_main_step_008000.json")["results"]
    wm = J("world_model.json"); bcz = J("board_causal.json"); lad = J("ladder_summary.json"); cov = J("concept_coverage.json")
    bc = J("block_circuit.json"); of = J("orientation_followup.json"); vm = J("vertical_map.json"); ph = J("vertical_posthoc.json")
    ta = J("ns_block_testA.json"); sw = J("sweep_summary.json"); sae = J("sae.json")
    nsq, nsr = json.loads((ROOT / "ns" / "report.json").read_text()), json.loads((ROOT / "ns2" / "report.json").read_text())

    # model and training
    m = cfg["model"]
    put("n_layer", m["n_layer"], "i"); put("d_model", m["d_model"], "i"); put("n_head", m["n_head"], "i"); put("d_ff", m["d_ff"], "i")
    put("params", tr["params"], "m1"); put("steps", cfg["train"]["steps"], "i"); put("train_games", cfg["data"]["splits"]["train"][0], "i")
    put("teacher_depth", cfg["teacher"]["depth"], "i"); put("agree", tr["curve"][-1]["agree"], "p0")
    put("win_d10", play["teacher_d10"]["win"], "p0"); put("draw_d10", play["teacher_d10"]["draw"], "p0"); put("loss_d10", play["teacher_d10"]["loss"], "p0")
    put("win_random", play["random"]["win"], "p0"); put("train_minutes", tr["curve"][-1]["time"] / 60, "f0")

    # world model and board edits
    pts = wm["points"]; i3 = pts.index(wm["best_point"])
    put("rel_colour", wm["probe"][i3]["rel"]["colour_acc"], "p1"); put("abs_colour", wm["probe"][i3]["abs"]["colour_acc"], "p0")
    put("ply_colour", wm["ply_baseline"]["colour_acc"], "p0"); put("best_point", wm["best_point"])
    br = bcz["result"]
    put("edit_n", br["n"], "i"); put("edit_rel", br["change_rel"], "p0"); put("edit_irr", br["change_irr"], "p0")
    put("edit_spec", br["spec"], "f2"); put("edit_lo", br["ci95"][0], "f2"); put("edit_hi", br["ci95"][1], "f2")

    # size ladder: recompute the correlation from the individual runs
    runs = [(r["colour_acc"], r["spec"], e["size"]) for e in lad for r in e["runs"]]
    rr = float(np.corrcoef([a for a, _, _ in runs], [s for _, s, _ in runs])[0, 1])
    assert len(runs) == sum(e["n_models"] for e in lad) == 43, len(runs)
    put("n_ladder", len(runs), "i"); put("ladder_r", rr, "f2")
    by = {e["size"]: e for e in lad}
    put("pass_6x128", by["L6d128"]["n_pass"], "i"); put("pass_4x192", by["L4d192"]["n_pass"], "i")

    # blocking circuit (s), frozen
    h = hashlib.sha256((R / "block_circuit.json").read_bytes()).hexdigest()[:16]
    assert h in (ROOT / "docs" / "LOG.md").read_text(), "frozen circuit hash not in docs/LOG.md"
    f = bc["faithfulness"]; pv = bc["pairs"]["val"]
    put("bp_cand", pv["n_candidates"], "i"); put("bp_n", pv["n_pairs"], "i"); put("bp_acc", pv["clean_block_acc"], "p0")
    put("c200", f["s1_effect"], "p0"); put("c200_rand", f["s2_random_effects_p50_p95"][1], "p0"); put("c200_restore", f["s3_restoration"], "p0")
    so = f["s6_circuit_size_by_orientation"]
    put("v_circuit", so["vertical"]["size"], "i"); put("c_size", bc["circuit"]["size"], "i")
    # orientations (t), layers 0-4
    o = of["layers0-4"]
    for k in ("vertical", "horizontal", "diagonal"):
        put(f"n80_{k}", o[k]["T1"]["n80"], "i"); put(f"d80_{k}", o[k]["T2"]["d80"], "i")
        put(f"head_{k}", o[k]["T3"]["top_effect"], "p0")
    put("d80_v_conf", o["vertical"]["T2"]["confirm_effect"], "p0"); put("top50_h", dict(o["horizontal"]["T1"]["curve"])[50], "p0")
    # vertical end to end (u)
    assert vm["circuit"]["size"] == so["vertical"]["size"], "vertical circuit did not reproduce"
    R_ = vm["u3_alarms"]["neurons"]
    put("n_alarm", len(R_), "i"); put("alarm_eff", vm["readout_confirm_effect"], "p0"); put("alarm_share", vm["u3_alarms"]["share_promote_equals_best_col"], "p0")
    put("dirs_move_alarm", vm["u2_readout_moved"]["weighted_mean"], "p0"); put("dirs_eff", vm["directions_confirm_effect"], "p0")
    u1 = vm["u1_attention"]; put("att_same", u1["same_column_share"], "p0"); put("att_unif", u1["uniform_baseline"], "p0")
    pa = ph["attention_vertical_pairs"]; put("att_opp", pa["last_mover_any"], "p0"); put("att_p1", pa["last_mover_prev1"], "p0"); put("att_p2", pa["last_mover_prev2"], "p0")
    put("att_same_all", ph["attention_all_positions"]["last_mover_same_col"], "p0")
    au = [ph["direction_auroc"][l]["vertical threat on the last-move column (run 3, cell above empty)"] for l in ("1", "2", "4")]
    put("auroc_lo", min(au), "f2"); put("auroc_hi", max(au), "f2")
    holds = [vm["u1_attention"]["holds"], vm["u2_readout_moved"]["holds"], vm["u3_alarms"]["holds"], vm["u4_direction_meaning"]["holds"],
             vm["u5_switches"]["i_holds"], vm["u5_switches"]["ii_holds"], vm["u5_switches"]["iii_holds"]]
    put("u_total", len(holds), "i"); put("u_failed", sum(not h for h in holds), "i")
    rho = vm["u4_direction_meaning"]["spearman"]; put("rho_max", max(abs(v) for v in rho.values()), "f2")
    A = vm["u5_switches"]["accuracy"]; N = vm["u5_switches"]["n_positions"]
    for s in ("none", "head", "directions", "readout"):
        for k in ("vertical", "horizontal", "diagonal", "control"):
            put(f"acc_{s}_{k}", A[s][k], "p0")
    put("n_vert_pos", N["vertical"], "i"); put("n_ctrl_pos", N["control"], "i")
    put("rand_drop", max(A["none"]["vertical"] - vm["u5_switches"]["random_directions_median"]["vertical"],
                         A["none"]["vertical"] - vm["u5_switches"]["random_readout_median"]["vertical"]), "pt0")
    # agent descriptions: Test A and the studies
    put("ta_overlap", len(ta["overlap"]), "i"); put("ta_real", ta["n_real_units"], "i"); put("ta_chance", ta["expected_overlap_by_chance_poles"], "f0")
    put("ta_tact", len(ta["units_with_tactic_agreement_ge_0.5"]), "i")
    put("ta_tact_circ", sum(x["in_circuit_neuron"] for x in ta["units_with_tactic_agreement_ge_0.5"]), "i")
    real = [r for rep in (nsq, nsr) for r in rep["rows"] if r["kind"] == "neuron"]
    rnd = [r for rep in (nsq, nsr) for r in rep["rows"] if r["kind"] != "neuron"]
    put("ns_real", len(real), "i"); put("ns_good", sum(r["test_f1"] >= 0.5 for r in real), "i")
    put("ns_rand", len(rnd), "i"); put("ns_rand_good", sum(r["test_f1"] >= 0.5 for r in rnd), "i")
    assert (V["ns_good"][0], V["ns_rand_good"][0]) == (44, 9)
    vm_ids = {(n["layer"], n["neuron"], n["pole"]) for n in vm["circuit"]["neurons"]}
    vm_rank = {(n["layer"], n["neuron"], n["pole"]): i for i, n in enumerate(vm["circuit"]["neurons"])}
    desc = sorted([x for x in ta["all"] if (x["layer"], x["neuron"], x["pole"]) in vm_ids], key=lambda x: vm_rank[(x["layer"], x["neuron"], x["pole"])])
    put("ta_vert", len(desc), "i")
    put("n_neurons", m["n_layer"] * m["d_ff"], "i")
    first = re.split(r"(?<=\.)\s(?=[A-Z])", desc[0]["description"])[0]
    cut = min([i for i in (first.find(" ("), first.find(";"), first.find(", i.e."), first.find(":")) if i > 40] or [len(first)])
    put("desc_example", first[:cut].rstrip("."))
    named = [x for x in desc if any(w in x["description"].lower() for w in ("must-block", "must block", "threat", "immediate win"))]
    put("ta_vert_named", len(named), "i")
    assert len(named) == len(desc), "the post says every description in the vertical circuit names a threat"
    put("ta_vert_f1_lo", min(x["test_f1_reported"] for x in desc), "f2"); put("ta_vert_f1_hi", max(x["test_f1_reported"] for x in desc), "f2")
    # Test B (s, S7): the blind run on the 20 most important circuit poles, 20 matched decoys, 10 random directions
    tb = J("ns3_testB.json"); P = tb["primary"]; rows = tb["rows"]
    grp = lambda g, rs=rows: [r for r in rs if r["group"] == g]
    hit = lambda rs: sum(r["tactic_agreement"] >= 0.5 for r in rs)
    assert (len(grp("circuit")), len(grp("decoy")), len(grp("random"))) == (20, 20, 10)
    assert abs(hit(grp("circuit")) / 20 - P["s_B1"]["circuit_share_ge_0.5"]) < 1e-9 and abs(hit(grp("decoy")) / 20 - P["s_B1"]["decoy_share_ge_0.5"]) < 1e-9
    assert P["s_B1"]["holds"] and P["s_B3"]["holds"] and not P["s_B2"]["holds"], "the post says s-B1 and s-B3 hold and s-B2 fails"
    put("tb_circ_hit", hit(grp("circuit")), "i"); put("tb_dec_hit", hit(grp("decoy")), "i"); put("tb_rand_hit", hit(grp("random")), "i")
    put("tb_txt_circ", sum(r["textcheck_yes"] for r in grp("circuit")), "i"); put("tb_txt_dec", sum(r["textcheck_yes"] for r in grp("decoy")), "i")
    s3 = P["s_B3"]
    put("tb_f1_circ", s3["circuit_median"], "f2"); put("tb_f1_dec", s3["decoy_median"], "f2"); put("tb_f1_diff", s3["diff"], "f2")
    put("tb_f1_lo", s3["ci95"][0], "f2"); put("tb_f1_hi", s3["ci95"][1], "f2")
    put("tb_p90_diff", P["s_B3_p90_secondary"]["diff"], "f2"); put("tb_p80_diff", P["s_B3_p80_secondary"]["diff"], "f2")
    put("tb_conf_circ", P["confidence"]["circuit"]["medium"] + P["confidence"]["circuit"]["high"], "i")
    put("tb_conf_dec_low", P["confidence"]["decoy"]["low"], "i"); put("tb_conf_rand_low", P["confidence"]["random"]["low"], "i")
    miss = [r for r in grp("circuit") if r["tactic_agreement"] < 0.5]
    put("tb_miss", len(miss), "i"); put("tb_miss_l0", sum(r["layer"] == 0 for r in miss), "i")
    assert len(miss) - V["tb_miss_l0"][0] == 4, "Appendix I names two near-miss vertical and two horizontal misses"
    put("tb_miss_l0_f1", min(r["f1_p97"] for r in miss if r["layer"] == 0), "f2")
    put("tb_hit_l5", sum(r["tactic_agreement"] >= 0.5 and r["layer"] == 5 for r in grp("circuit")), "i")
    put("tb_rb", len(tb["rule_breaks"]), "i")
    fu = [r for r in rows if not r["rule_break"]]
    put("tb_fu_circ_hit", hit(grp("circuit", fu)), "i"); put("tb_fu_circ_n", len(grp("circuit", fu)), "i")
    put("tb_fu_dec_hit", hit(grp("decoy", fu)), "i"); put("tb_fu_dec_n", len(grp("decoy", fu)), "i")
    put("tb_fu_diff", tb["followup_excluding_rule_breaks"]["s_B3"]["diff"], "f2")
    best = max(grp("circuit"), key=lambda r: r["tactic_agreement"])
    put("tb_best_ta", best["tactic_agreement"], "f2")
    put("tb_best_desc", re.split(r"(?<=[.:])\s", best["description"])[0].rstrip(".:"))
    # other concepts, appendix
    c = cov["coverage"]; put("n_concepts", cov["n_concepts"], "i")
    put("cov_neuron", c["neuron"]["share"], "p0"); put("cov_rot", c["rotation"]["share"], "p0"); put("cov_probe", c["probe"]["share"], "p0")
    put("sweep_held", sum(bool(v.get("holds")) for k, v in sw["predictions"].items() if k in ("W1", "W2", "W3")), "i")
    tot_lat = len(sae["layers"]) * sae["latents_per_layer"]
    put("sae_dead", sae["sae_dead_or_rare"] / tot_lat, "p0")

    FIG = {
        "board": {"points": pts, "rel": [p["rel"]["colour_acc"] for p in wm["probe"]], "abs": [p["abs"]["colour_acc"] for p in wm["probe"]],
                  "ply": wm["ply_baseline"]["colour_acc"]},
        "curves": {k: {"neurons": o[k]["T1"]["curve"], "dirs": o[k]["T2"]["curve"], "target": o[k]["target"], "n80": o[k]["T1"]["n80"],
                       "d80": o[k]["T2"]["d80"]} for k in ("vertical", "horizontal", "diagonal")},
        "switch": {"acc": A, "n": N},
        "circuit": {"att_opp": pa["last_mover_any"], "head_eff": o["vertical"]["T3"]["top_effect"], "d80": o["vertical"]["T2"]["d80"],
                    "dirs_eff": o["vertical"]["T2"]["confirm_effect"], "n_alarm": len(R_), "alarm_eff": vm["readout_confirm_effect"],
                    "alarm_share": vm["u3_alarms"]["share_promote_equals_best_col"], "v_circuit": so["vertical"]["size"],
                    "acc": {k: A[k]["vertical"] for k in ("none", "head", "directions", "readout")}},
        "ladder": [{"size": s, "colour": a, "spec": sp} for a, sp, s in runs],
        "coverage": {k: {"share": c[k]["share"], "ci": c[k]["ci95"]} for k in ("neuron", "rotation", "probe")},
        "described": [{"id": x["id"], "layer": x["layer"], "neuron": x["neuron"], "pole": x["pole"], "f1": x["test_f1_reported"],
                       "rank": vm_rank[(x["layer"], x["neuron"], x["pole"])] + 1,
                       "text": x["description"]} for x in desc],
        "testB": [{"u": r["unit"], "g": r["group"], "l": r["layer"], "n": r["neuron"], "pole": r["pole"], "ta": round(r["tactic_agreement"], 3),
                   "c": r["best_block_concept"], "f1": round(r["f1_p97"], 3), "txt": r["textcheck_yes"], "conf": r["confidence"],
                   "rb": r["rule_break"], "rank": r["rank"], "text": r["description"]} for r in rows],
    }

    def fmt(v, f):
        return {"i": lambda: f"{v:,}", "m1": lambda: f"{v / 1e6:.1f}M", "p0": lambda: f"{100 * v:.0f}%", "p1": lambda: f"{100 * v:.1f}%",
                "pt0": lambda: f"{100 * v:.0f}", "f0": lambda: f"{v:.0f}", "f2": lambda: f"{v:.2f}", "s": lambda: str(v)}[f]()

    def sub(mt):
        k, f = mt.group(1), mt.group(2)
        assert k in V, f"no value for {{{{{k}}}}}"
        v, f0 = V[k]
        return fmt(v, f or f0)
    tpl = (OUT / "post.tpl.html").read_text()
    html = re.sub(r"\{\{([a-zA-Z0-9_]+)(?:\|([a-z0-9]+))?\}\}", sub, tpl)
    assert "{{" not in html
    (OUT / "index.html").write_text(html)
    # the companion demo page (the live model and guided tour), linked from the post
    dtpl = (OUT / "demo" / "demo.tpl.html").read_text()
    dhtml = re.sub(r"\{\{([a-zA-Z0-9_]+)(?:\|([a-z0-9]+))?\}\}", sub, dtpl)
    assert "{{" not in dhtml
    (OUT / "demo" / "index.html").write_text(dhtml)
    unused = [k for k in V if "{{" + k not in tpl and "{{" + k not in dtpl]
    (OUT / "data").mkdir(exist_ok=True)
    (OUT / "data" / "figures.js").write_text("window.FIGURES = " + json.dumps(FIG) + ";\n")
    words = len(re.sub(r"<[^>]+>", " ", html.split('<section class="appendix"')[0].split("<main")[1]).split())
    print(f"built {OUT / 'index.html'}: {len(V)} values ({len(unused)} unused: {unused}); ladder r = {rr:.3f}; main text ~{words} words")


if __name__ == "__main__":
    main()
