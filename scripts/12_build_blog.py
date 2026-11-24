"""Build the blog post from result files.

Every number on the page comes from results/*.json (or configs/base.yaml) through {{key|fmt}} placeholders in
docs/blog/post.tpl.html; the build fails if a placeholder has no value. Direction claims made in the prose (which basis
wins, which prediction failed) are asserted here, so the text cannot go stale when results change.

Writes docs/blog/index.html, docs/blog/data/figures.js, and copies the demo files into docs/blog/demo/.
Light, stdlib-only work on result files; no model is run.
"""
import html
import json
import re
import shutil
import statistics as st
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = ROOT / "docs" / "blog"
CFG = yaml.safe_load((ROOT / "configs" / "base.yaml").read_text())
J = lambda name: json.loads((RES / name).read_text())

# reported by Tigges et al. 2026 (their abstract); not produced by this repository
GF = {"gf_ablated": "92%", "gf_cost": "1.2 to 2.2 points", "gf_modes": "69%", "gf_neurons": "about 5 million"}

spars, conc, modes = J("sparsity.json"), J("concepts_summary.json"), J("modes.json")
dyn, grp, act = J("dynamics.json")["checkpoints"], J("group_action.json")["concepts"], J("action.json")["poles"]
sweep, sae, play = J("sweep_summary.json"), J("sae.json"), J("play_main_step_008000.json")
train = J("train_curve_main.json")
cond = {c["condition"]: c for c in spars["conditions"]}
quad = spars["quadrants"]
WIDTHS = sweep["widths"]
BW = sweep["by_width"]


def mean_k(rows, key, k):
    return st.mean([[b for b in r["by_k"] if b["k"] == k][0][key] for r in rows])


def fam_rows(prefix):
    return [r for r in grp if r["concept"].startswith(prefix)]


blk, win = fam_rows("block_now"), fam_rows("win_now")
assert len(blk) == 7 and len(win) == 7
fn, fr = conc["families_neurons"], conc["families_random_rotation"]
FAMS = [("line", "Open lines (twos and threes)", False), ("land", "Landing cell of each column", False),
        ("cell", "Board cells (mine / theirs / empty)", False), ("opp_threat_r", "Opponent's threat cells", False),
        ("block_now", "Must block column c", False), ("win_now", "Win now in column c", False),
        ("last_col", "Column of the last move", True), ("full", "Column is full", False), ("ply", "Game phase", True)]
shares = {f: (fn[f]["n_ge_0.5"], fr[f]["n_ge_0.5"]) for f, _, _ in FAMS}
# claims made in the prose about which basis wins
for f in ("line", "land", "cell", "opp_threat_r", "block_now", "win_now", "last_col"):
    assert shares[f][0] > shares[f][1], f"neurons should win on {f}: {shares[f]}"
for f in ("full", "ply"):
    assert shares[f][0] < shares[f][1], f"rotations should win on {f}: {shares[f]}"
pred = sweep["predictions"]
assert all(not pred[k]["holds"] for k in ("W1", "W2", "W3")), "prose says W1-W3 failed"
for key, direction in (("cost_P5-P95", "up"), ("neuron_minus_rotation", "down"), ("share_top_mode_ge_0.9", "down")):
    for s in range(2):  # both seeds move the same way from the narrowest to the widest model
        a, b = BW["256"][key]["values"][s], BW["4096"][key]["values"][s]
        assert (b > a) == (direction == "up"), f"seed {s} disagrees on {key}"
w4 = [[b for b in r["by_k"] if b["k"] == 20][0] for r in blk]
assert all(b["true_ablated"] < b["true_random_mean"] - 0.03 for b in w4), "W4: concept neurons should beat random at k=20"

first = lambda pred_fn: next(r for r in dyn if pred_fn(r))
d_blk, d_win = first(lambda r: r["block_rate"] >= 0.85), first(lambda r: r["take_win_rate"] >= 0.90)
fin = dyn[-1]
assert d_blk["tracked"]["block_now_any"] < 0.5 and d_win["tracked"]["win_now_any"] < 0.5, "prose says behaviour precedes neurons"

cl = cond["band_P5-P95"]
cost_p5 = cond["intact"]["agree"] - cl["agree"]
single = [abs(p["true_ablated"] - p["true_intact"]) * 100 for p in act]
E = {"E1": cost_p5 < 0.05, "E2": conc["neurons"]["f1_sweep"]["share_ge_0.5"] >= 0.30 and conc["neurons"]["f1_sweep"]["share_ge_0.5"] > conc["random_rotation"]["f1_sweep"]["share_ge_0.5"],
     "E3": modes["summary_random_sample"]["modes_median"] <= 1, "E4": d_blk["tracked"]["block_now_any"] >= 0.5}
S1_p97 = sae["sae_p97"]["share_ge_0.5"] > sae["neuron_poles_p97"]["share_ge_0.5"]
S1_sw = sae["sae_sweep"]["share_ge_0.5"] > sae["neuron_poles_sweep"]["share_ge_0.5"]


def f_p(v, d=0): return f"{100 * v:.{d}f}%"
def f_pt(v, d=0): return f"{100 * v:.{d}f}"
def f_sg(v): return ("+" if v > 0 else "−" if v < 0 else "") + f"{abs(100 * v):.1f}"


def tick(ok): return "held" if ok else "did not hold"


V = {}
def put(k, v, fmt): V[k] = (v, fmt)


# setup
put("games_train", CFG["data"]["splits"]["train"][0], "i"); put("depth", CFG["teacher"]["depth"], "i")
put("params", train["params"], "m1"); put("neurons_main", CFG["model"]["n_layer"] * CFG["model"]["d_ff"], "i")
put("n_pos", conc["n_positions"], "i"); put("n_concepts", conc["n_concepts_used"], "i")
put("agree_main", train["curve"][-1]["agree"], "p0")
d10 = play["results"]["teacher_d10"]
put("win_d10", d10["win"], "p0"); put("draw_d10", d10["draw"], "p0"); put("loss_d10", d10["loss"], "p0")
put("take_win", fin["take_win_rate"], "p0"); put("block_rate", fin["block_rate"], "p0")
# sparsity
put("cost_p5", cost_p5, "pt0"); put("zeroed_p5", cl["frac_zeroed"], "p0")
put("agree_top64", cond["keep_top64"]["agree"], "p0"); put("agree_rand64", cond["keep_random64"]["agree"], "p0")
q = lambda k, w: quad[k][w]
put("gate_pos_firing", q("gate+ up+", "firing") + q("gate+ up-", "firing"), "p0")
put("gate_pos_all", q("gate+ up+", "all") + q("gate+ up-", "all"), "p0")
sp_rows = ""
for name, label in (("intact", "None (intact model)"), ("band_P25-P75", "Central 50% (P25 to P75)"), ("band_P10-P90", "Central 80% (P10 to P90)"),
                    ("band_P5-P95", "Central 90% (P5 to P95)"), ("band_P3-P97", "Central 94% (P3 to P97)")):
    c = cond[name]
    sp_rows += f'<tr><td>{label}</td><td class="n">{f_p(c["frac_zeroed"])}</td><td class="n">{f_p(c["agree"])}</td></tr>'
put("sparsity_rows", sp_rows, "raw")
# concepts
put("share_n", conc["neurons"]["f1_sweep"]["share_ge_0.5"], "p1"); put("share_r", conc["random_rotation"]["f1_sweep"]["share_ge_0.5"], "p1")
for f, nm in (("line", "line"), ("land", "land"), ("cell", "cell"), ("opp_threat_r", "thr"), ("block_now", "blk"), ("win_now", "win"),
              ("last_col", "last"), ("full", "full"), ("ply", "ply")):
    put(f"fam_{nm}_n", shares[f][0], "i"); put(f"fam_{nm}_r", shares[f][1], "i")
pi = conc["pole_independence_p97"]
put("pi_fam", pi["same_family"], "p0"); put("pi_fam_sh", pi["same_family_shuffled"], "p0")
# modes
ms, mf = modes["summary_random_sample"], modes["summary_featured"]
put("modes_median", ms["modes_median"], "f0"); put("top90", ms["share_top_mode_ge_0.9"], "p0"); put("top90_feat", mf["share_top_mode_ge_0.9"], "p0")
put("modes_single", ms["share_single_mode"], "p0"); put("modes_outside", ms["multi_mode_median_damage_outside_main"], "p0")
put("gf_modes", GF["gf_modes"], "s")
for k, v in GF.items(): put(k, v, "s")
# sweep
for w in WIDTHS:
    g = lambda key: BW[str(w)][key]["mean"]
    put(f"gap{w}", g("neuron_minus_rotation"), "sg"); put(f"agree_w{w}", g("val_agree"), "p1")
sw_rows = ""
for w in WIDTHS:
    b = BW[str(w)]
    sw_rows += (f'<tr><td class="n">{w:,}</td><td class="n">{b["params"]["mean"] / 1e6:.1f}M</td><td class="n">{f_p(b["val_agree"]["mean"], 1)}</td>'
                f'<td class="n">{f_pt(b["cost_P5-P95"]["mean"], 1)}</td><td class="n">{f_p(b["share_f1_ge_0.5_neurons"]["mean"], 1)} / {f_p(b["share_f1_ge_0.5_rotation"]["mean"], 1)}</td>'
                f'<td class="n">{f_p(b["share_top_mode_ge_0.9"]["mean"])}</td></tr>')
put("sweep_rows", sw_rows, "raw")
rho = lambda k: f"{pred[k]['spearman_vs_log_width']:+.1f}".replace("-", "−")
pred_rows = (f'<tr><td>W1</td><td>Zeroing the weak activations costs less as layers widen</td><td>It costs more: {f_pt(BW["256"]["cost_P5-P95"]["mean"], 0)} points at 256, {f_pt(BW["4096"]["cost_P5-P95"]["mean"], 0)} at 4,096</td></tr>'
             f'<tr><td>W2</td><td>The neuron advantage over random directions grows, and is positive at 4,096</td><td>It shrinks and turns negative: {f_sg(BW["256"]["neuron_minus_rotation"]["mean"])} to {f_sg(BW["4096"]["neuron_minus_rotation"]["mean"])} points</td></tr>'
             f'<tr><td>W3</td><td>The share of poles with one dominant mode grows</td><td>It falls: {f_p(BW["256"]["share_top_mode_ge_0.9"]["mean"])} to {f_p(BW["4096"]["share_top_mode_ge_0.9"]["mean"])}</td></tr>')
put("pred_rows", pred_rows, "raw")
# action / group
put("single_med", st.median(single), "f1"); put("n_action", len(act), "i")
put("blk_intact", st.mean(r["true_intact"] for r in blk), "p0")
for k in (5, 20, 50):
    put(f"blk_off{k}", mean_k(blk, "true_ablated", k), "p0")
put("blk_rand20", mean_k(blk, "true_random_mean", 20), "p0"); put("blk_on20", mean_k(blk, "false_clamped", 20), "p0")
put("blk_false", st.mean(r["false_intact"] for r in blk), "p0")
put("win_intact", st.mean(r["true_intact"] for r in win), "p0"); put("win_off20", mean_k(win, "true_ablated", 20), "p0")
put("win_rand20", mean_k(win, "true_random_mean", 20), "p0"); put("win_on20", mean_k(win, "false_clamped", 20), "p0")
put("win_false", st.mean(r["false_intact"] for r in win), "p0")
# dynamics
put("step_blk", d_blk["step"], "i"); put("f1_blk_at", d_blk["tracked"]["block_now_any"], "f2"); put("f1_blk_end", fin["tracked"]["block_now_any"], "f2")
put("step_win", d_win["step"], "i"); put("f1_win_at", d_win["tracked"]["win_now_any"], "f2"); put("f1_win_end", fin["tracked"]["win_now_any"], "f2")
# SAE
put("sae_live", sae["sae_live_latents"], "i"); put("sae_total", sae["sae_live_latents"] + sae["sae_dead_or_rare"], "i")
put("sae_dead", sae["sae_dead_or_rare"] / (sae["sae_live_latents"] + sae["sae_dead_or_rare"]), "p0")
put("sae_p97", sae["sae_p97"]["share_ge_0.5"], "p1"); put("nrn_p97", sae["neuron_poles_p97"]["share_ge_0.5"], "p1")
put("sae_sw", sae["sae_sweep"]["share_ge_0.5"], "p1"); put("nrn_sw", sae["neuron_poles_sweep"]["share_ge_0.5"], "p1")
put("sae_fvu_max", max(l["fvu_analysis"] for l in sae["layers"]), "p0"); put("sae_fvu_min", min(l["fvu_analysis"] for l in sae["layers"]), "p1")
# pre-registered outcomes
pr = [("E1", "Zeroing each neuron's central 90% costs under 5 points of agreement", E["E1"], f"{f_pt(cost_p5)} points"),
      ("E2", "At least 30% of poles match a concept, and more than random directions", E["E2"], f"{f_p(conc['neurons']['f1_sweep']['share_ge_0.5'], 1)} of poles, against {f_p(conc['random_rotation']['f1_sweep']['share_ge_0.5'], 1)} for random directions"),
      ("E3", "The median pole has one dominant mode", E["E3"], f"median {ms['modes_median']:.0f} modes for random poles, {mf['modes_median']:.0f} for the best concept-matched poles"),
      ("E4", "Dedicated neurons appear before the behaviour is reliable", E["E4"], f"blocking reached 85% at step {d_blk['step']:,}, when the best match had F1 {d_blk['tracked']['block_now_any']:.2f}"),
      ("W1", "Zeroing the weak activations costs less as layers widen", pred["W1"]["holds"], "rose with width"),
      ("W2", "The neuron advantage over random directions grows with width", pred["W2"]["holds"], "fell with width"),
      ("W3", "The one-dominant-mode share grows with width", pred["W3"]["holds"], "fell with width"),
      ("W4", "Switching off the top-k concept neurons lowers behaviour more than k random ones", True, f"at k = 20, blocking fell to {f_p(mean_k(blk, 'true_ablated', 20))} against {f_p(mean_k(blk, 'true_random_mean', 20))} for random neurons"),
      ("S1", "SAE latents match concepts more often than neurons", None, f"yes at p97 ({f_p(sae['sae_p97']['share_ge_0.5'], 1)} against {f_p(sae['neuron_poles_p97']['share_ge_0.5'], 1)}); no over the threshold sweep ({f_p(sae['sae_sweep']['share_ge_0.5'], 1)} against {f_p(sae['neuron_poles_sweep']['share_ge_0.5'], 1)})")]
put("n_e_fail", sum(not v for v in E.values()), "i"); put("n_e_total", len(E), "i"); put("n_ckpt", len(dyn), "i")
put("prereg_rows", "".join(f'<tr><td>{a}</td><td>{b}</td><td>{"mixed" if c is None else tick(c)}</td><td>{d}</td></tr>' for a, b, c, d in pr), "raw")

# ---------------- figure data ----------------
FIG = {"families": [{"label": l, "neurons": shares[f][0], "rotation": shares[f][1], "readable_from_embeddings": t} for f, l, t in FAMS],
       "sweep": {"widths": WIDTHS, "panels": [
           {"key": "cost", "title": "Accuracy lost by zeroing the central 90%", "unit": "points", "scale": 100, "values": [BW[str(w)]["cost_P5-P95"]["values"] for w in WIDTHS]},
           {"key": "gap", "title": "Neurons minus random directions matching a concept", "unit": "points", "scale": 100, "values": [BW[str(w)]["neuron_minus_rotation"]["values"] for w in WIDTHS]},
           {"key": "top", "title": "Poles with one dominant mode", "unit": "%", "scale": 100, "values": [BW[str(w)]["share_top_mode_ge_0.9"]["values"] for w in WIDTHS]}]},
       "group": {"ks": [b["k"] for b in blk[0]["by_k"]], "concepts": {}},
       "dynamics": [{"step": r["step"], "block": r["block_rate"], "win": r["take_win_rate"], "f1_block": r["tracked"]["block_now_any"], "f1_win": r["tracked"]["win_now_any"]} for r in dyn]}
for name, rows in (("block", blk), ("win", win)):
    FIG["group"]["concepts"][name] = {
        "intact": st.mean(r["true_intact"] for r in rows), "false_intact": st.mean(r["false_intact"] for r in rows),
        "off": [mean_k(rows, "true_ablated", k) for k in FIG["group"]["ks"]], "random": [mean_k(rows, "true_random_mean", k) for k in FIG["group"]["ks"]],
        "on": [mean_k(rows, "false_clamped", k) for k in FIG["group"]["ks"]],
        "off_cols": [[[b for b in r["by_k"] if b["k"] == k][0]["true_ablated"] for r in rows] for k in FIG["group"]["ks"]],
        "on_cols": [[[b for b in r["by_k"] if b["k"] == k][0]["false_clamped"] for r in rows] for k in FIG["group"]["ks"]]}


def render(tpl):
    def sub(m):
        key, fmt = m.group(1), m.group(2) or "s"
        assert key in V, f"no value for {{{{{key}}}}}"
        v, f = V[key]
        f = fmt if fmt != "s" or f == "s" else f  # a fmt in the template overrides; otherwise the registered one
        return {"i": lambda: f"{v:,}", "m1": lambda: f"{v / 1e6:.1f}M", "p0": lambda: f_p(v), "p1": lambda: f_p(v, 1), "pt0": lambda: f_pt(v),
                "f0": lambda: f"{v:.0f}", "f1": lambda: f"{v:.1f}", "f2": lambda: f"{v:.2f}", "sg": lambda: f_sg(v), "raw": lambda: v, "s": lambda: str(v)}[f]()
    out = re.sub(r"\{\{([a-zA-Z0-9_]+)(?:\|([a-z0-9]+))?\}\}", sub, tpl)
    assert "{{" not in out
    return out


def main():
    (OUT / "data").mkdir(parents=True, exist_ok=True)
    (OUT / "assets").mkdir(exist_ok=True)
    (OUT / "demo").mkdir(exist_ok=True)
    (OUT / "index.html").write_text(render((OUT / "post.tpl.html").read_text()))
    (OUT / "data" / "figures.js").write_text("window.FIGURES = " + json.dumps(FIG) + ";\n")
    for f in ("c4model.js", "concepts.js", "demo.js", "demo.css", "model.json", "model.bin", "poles.json", "groups.json", "parts.json"):
        shutil.copy(ROOT / "web" / f, OUT / "demo" / f)
    print("built", OUT / "index.html", "| values:", len(V))


if __name__ == "__main__":
    main()
