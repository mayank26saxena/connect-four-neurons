"""Aggregate the size ladder (PLAN addendum l): one row per size with parameters, teacher agreement, board readability and the
board test, over seeds. Reads results/{ladder,small}/*/board_causal.json and the training curves; writes results/ladder_summary.json."""
import json
import statistics as st

from c4n import config

ROOT = config.ROOT
SIZES = [("L1d64", "ladder"), ("L1d128", "ladder"), ("L2d64", "ladder"), ("L2d128", "ladder"), ("L3d64", "ladder"), ("L3d128", "small"),
         ("L6d128", "ladder"), ("L4d192", "ladder"), ("L4d256", "ladder"), ("L6d256", "main"), ("L6d256r", "ladder")]  # L6d256r: seeds 2, 3 of the 6,000-step recipe


def load_run(size, kind, s):
    size = size.rstrip("r") if size == "L6d256r" else size
    if kind == "main":
        rd, curve = ROOT / "results", ROOT / "results" / "train_curve_main.json"
    elif kind == "small":
        rd = ROOT / "results" / "small" / f"s{s}"; curve = rd / f"train_curve_s{s}.json"
    else:
        rd = ROOT / "results" / "ladder" / f"{size}_s{s}"; curve = rd / f"train_curve_{size}_s{s}.json"
    bc = rd / "board_causal.json"
    if not bc.exists():
        return None
    d = json.loads(bc.read_text())
    c = json.loads(curve.read_text()) if curve.exists() else None
    agree = (c["curve"][-1]["agree"] if isinstance(c, dict) else c[-1]["agree"]) if c else None
    params = c["params"] if isinstance(c, dict) and "params" in c else None
    return {"seed": s, "agree": agree, "colour_acc": d["board"]["colour_acc"], "best_point": d["board"]["best_point"], "n_pairs": d["result"]["n"],
            "spec": d["result"]["spec"], "ci95": d["result"]["ci95"], "dir": d["result"]["dir"], "keep": d["result"]["keep_irr"],
            "readable": d["verdict"]["readable_board"], "k_a": d["verdict"]["k_a"], "random_follow": d["result"]["random_report"]["follow"], "params": params}


def main():
    out = []
    for size, kind in SIZES:
        seeds = [2, 3] if size == "L6d256r" else (range(1, 6) if kind != "main" else [0])
        runs = [r for r in (load_run(size, kind, s) for s in seeds) if r]
        if not runs:
            continue
        m = lambda k: st.mean(r[k] for r in runs if r[k] is not None) if any(r[k] is not None for r in runs) else None
        out.append({"size": size, "n_models": len(runs), "params": next((r["params"] for r in runs if r["params"]), None), "agree": m("agree"), "colour_acc": m("colour_acc"),
                    "spec_mean": m("spec"), "spec_min": min(r["spec"] for r in runs), "dir": m("dir"), "keep": m("keep"),
                    "n_readable": sum(r["readable"] for r in runs), "n_pass": sum(r["k_a"] for r in runs), "runs": runs})
    (ROOT / "results" / "ladder_summary.json").write_text(json.dumps(out, indent=1))
    for r in out:
        print(f'{r["size"]:7} models {r["n_models"]} params {r["params"]} agree {r["agree"] and round(r["agree"], 3)} colour {round(r["colour_acc"], 3)} '
              f'spec {round(r["spec_mean"], 3)} (min {round(r["spec_min"], 3)}) dir {round(r["dir"], 2)} readable {r["n_readable"]}/{r["n_models"]} pass {r["n_pass"]}/{r["n_models"]}')


if __name__ == "__main__":
    main()
