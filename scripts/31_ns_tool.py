"""Neuron Scientist, step 2: the describing agent's tools (PLAN.md addendum (q), docs/NEURON_SCIENTIST.md).

All tools read the dev split only. Usage: uv run python scripts/31_ns_tool.py <command> ...
  units                              the units, their layer and pole, dev-metric calls used, whether submitted
  examples U07 [--n 40] [--band B]   dev positions across 10 activation bands (or one band, 0 = lowest .. 9 = top 0.1%)
  act U07 --moves 3,3,4              the unit's pole activation after each move of a sequence you write
  facts --moves 3,3,4                board, landing cells, immediate wins / must-blocks, threat cells, teacher scores
  steer U07 --moves 3,3,4 [--to max|zero|<value>]    move probabilities with the unit set to a value at the last position
  score U07 prog.py                  THE DEV METRIC (budgeted): detection F1 / AUROC, simulation recovery, misclassified examples
  synth U07 --moves 3,3,4            does this position beat the unit's dev maximum?
  submit U07 final.json              validate and store the final description
Moves are columns 0-6, separated by commas; "" is the empty board.
"""
import argparse
import json
import sys
import time

import numpy as np

from c4n import config
from c4n import engine as E
from c4n import ns

CFG = config.load()
NC = ns.ns_config(CFG)
BANDS = [0, 50, 80, 90, 95, 97, 98, 99, 99.5, 99.9, 100]


def parse_moves(s):
    s = (s or "").strip()
    mv = [int(x) for x in s.split(",") if x.strip() != ""] if s else []
    h = [0] * 7
    for c in mv:
        if not 0 <= c <= 6 or h[c] >= 6:
            sys.exit(f"illegal move sequence: column {c} is not playable")
        h[c] += 1
    return mv


def legal_game_error(mv):
    """(r) A synthesis sequence must be a real, unfinished game with at least min_ply stones: no move may complete a four."""
    if len(mv) < NC["min_ply"]:
        return f"it has fewer than {NC['min_ply']} stones"
    g = [[0] * 7 for _ in range(6)]; h = [0] * 7
    for i, c in enumerate(mv):
        r = h[c]; p = i % 2 + 1; g[r][c] = p; h[c] += 1
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            n = 1
            for s in (1, -1):
                rr, cc = r + s * dr, c + s * dc
                while 0 <= rr < 6 and 0 <= cc < 7 and g[rr][cc] == p:
                    n += 1; rr += s * dr; cc += s * dc
            if n >= 4:
                return f"move {i + 1} completes a four, so the game is already over"
    return None


def ctx():
    units = ns.units()
    us = [u["id"] for u in units]
    return units, us, ns.unit_key(), ns.stats()


def work_dir(u):
    d = ns.NS / "work" / u
    d.mkdir(parents=True, exist_ok=True)
    return d


def calls_used(u):
    f = ns.NS / "work" / u / "dev_calls.jsonl"
    return sum(1 for _ in open(f)) if f.exists() else 0


def show(b, extra=""):
    print(b.render() + (("   " + extra) if extra else ""))


def cmd_units(a):
    units, us, key, st = ctx()
    print("unit  layer pole  dev-calls  submitted")
    for u in units:
        sub = (ns.NS / "descriptions" / f"{u['id']}.json").exists()
        print(f"{u['id']:5} {u['layer']:>5} {u['pole']:>4}  {calls_used(u['id'])}/{NC['max_dev_calls']:<6}  {'yes' if sub else ''}")


def dev_data():
    moves, scores, lengths = ns.load_games(ns.DEV_SPLIT, NC["n_games"])
    return moves, scores, lengths


def cmd_examples(a):
    units, us, key, st = ctx()
    j = us.index(a.unit)
    S = np.load(ns.CACHE / "dev_acts.npy")[:, j]
    sign = st[a.unit]["sign"]
    pole = sign * S
    moves, _, lengths = dev_data()
    bs = ns.BoardSet(moves, lengths)
    el = ns.eligible(lengths, NC["min_ply"])  # (r) only eligible positions are shown and banded
    edges = np.percentile(pole[el], BANDS)
    rng = np.random.default_rng(a.seed)
    bands = [a.band] if a.band is not None else list(range(10))
    per = max(1, a.n // len(bands))
    print(f"{a.unit}: layer {st[a.unit]['layer']}, pole {'+' if sign > 0 else '-'}; fires when pole activation > "
          f"{sign * st[a.unit]['thr']:.3f} (dev firing rate {st[a.unit]['fire_rate']:.1%}); dev max {st[a.unit]['dev_max_pole']:.3f}")
    if NC["min_ply"]:
        print(f"(only positions with at least {NC['min_ply']} stones on the board count; earlier positions are never scored)")
    for k in bands:
        lo, hi = edges[k], edges[k + 1]
        idx = np.flatnonzero((pole >= lo) & (pole <= hi) & el)
        if len(idx) == 0:
            continue
        print(f"\n=== band {k}: pole-activation percentile {BANDS[k]}-{BANDS[k + 1]} ({lo:.3f} to {hi:.3f}) ===")
        for i in rng.choice(idx, min(per, len(idx)), replace=False):
            b = bs.board(int(i))
            fire = "FIRES" if ns.fires_from(np.array([S[i]]), st, a.unit)[0] else ""
            print(f"\n[pos {i}] pole act {pole[i]:.3f} {fire}  moves: {','.join(map(str, b.moves))}  "
                  f"last move col {b.last_col}  my immediate wins {sorted(b.my_playable_wins)}  must-block {sorted(b.their_playable_wins)}")
            show(b)


def cmd_act(a):
    units, us, key, st = ctx()
    mv = parse_moves(a.moves)
    model = ns.load_web_model()
    s = ns.acts_for_sequence(model, mv, a.unit, key)
    sign = st[a.unit]["sign"]
    print(f"{a.unit} pole activation after each move (fires above {sign * st[a.unit]['thr']:.3f}; dev max {st[a.unit]['dev_max_pole']:.3f}):")
    for t, v in enumerate(s):
        fire = "FIRES" if ns.fires_from(np.array([v]), st, a.unit)[0] else ""
        if t < NC["min_ply"]:
            fire = "(not scored: fewer than %d stones)" % NC["min_ply"]
        print(f"  after {t:2d} moves ({','.join(map(str, mv[:t])) or 'empty'}): {sign * v:.3f} {fire}")
    show(ns.board_from_moves(mv))


def cmd_facts(a):
    mv = parse_moves(a.moves)
    b = ns.board_from_moves(mv)
    show(b)
    print(f"ply {b.ply}, me = {'first' if b.me_first else 'second'} player, last move column {b.last_col} row {b.last_row}")
    print(f"landing rows: {[b.landing(c) for c in range(7)]}  legal: {b.legal}")
    print(f"my immediate wins (landing cells completing four for me): {sorted(b.my_playable_wins)}")
    print(f"must-block cells (landing cells completing four for them): {sorted(b.their_playable_wins)}")
    print(f"all my threat cells: {sorted(b.my_wins)}\nall their threat cells: {sorted(b.their_wins)}")
    try:
        sc = E.score_moves(np.array(mv, dtype=np.int8), 8)
        print("teacher scores (depth 8; higher is better for me; -32768 = illegal):", sc.tolist())
    except ValueError:
        print("teacher: position is already decided")


def cmd_steer(a):
    units, us, key, st = ctx()
    mv = parse_moves(a.moves)
    model = ns.load_web_model()
    to = a.to
    val = st[a.unit]["dev_max_raw"] if to == "max" else (0.0 if to == "zero" else float(to) * st[a.unit]["sign"])
    p0 = ns.move_probs(model, mv)
    p1 = ns.move_probs(model, mv, a.unit, key, val)
    s = ns.acts_for_sequence(model, mv, a.unit, key)[-1]
    print(f"{a.unit}: raw activation here {s:.3f} -> set to {val:.3f}")
    print("column      " + "  ".join(f"{c:>5}" for c in range(7)))
    print("intact      " + "  ".join(f"{x:5.2f}" for x in p0))
    print("steered     " + "  ".join(f"{x:5.2f}" for x in p1))
    print("change      " + "  ".join(f"{x:+5.2f}" for x in p1 - p0))
    show(ns.board_from_moves(mv))


def cmd_score(a):
    units, us, key, st = ctx()
    used = calls_used(a.unit)
    if used >= NC["max_dev_calls"]:
        sys.exit(f"{a.unit}: dev-metric budget used ({used}/{NC['max_dev_calls']}); submit your best description")
    code = open(a.program).read()
    fires_fn, level_fn = ns.load_program(code)
    j = us.index(a.unit)
    moves, _, lengths = dev_data()
    ng = NC["dev_score_games"]  # the feedback loop scores the first dev_score_games dev games (cheaper; verification uses all)
    moves, lengths = moves[:ng], lengths[:ng]
    S = np.load(ns.CACHE / "dev_acts.npy")[: int(lengths.sum()), j]
    bs = ns.BoardSet(moves, lengths)
    t0 = time.time()
    pred_v = ns.run_program(fires_fn, bs)
    el = ns.eligible(lengths, NC["min_ply"])  # (r) detection is scored on eligible positions only
    fire = ns.fires_from(S, st, a.unit) & el
    pred = (pred_v >= 0.5) & el
    f1, prec, rec = ns.f1(pred[el], fire[el])
    au = ns.auroc(pred_v[el], fire[el])
    # simulation on the first dev_sim_games games; level map fitted on the remaining dev games
    n_sim = NC["dev_sim_games"]
    cut = int(lengths[:n_sim].sum())
    lv = ns.run_program(level_fn, bs) if level_fn else pred_v
    m = ns.level_map(lv[cut:], S[cut:])
    model = ns.load_web_model()
    sim = ns.kl_recovery(model, moves[:n_sim], lengths[:n_sim], a.unit, key, ns.apply_level_map(m, lv[:cut]), S[:cut])
    ceil_m = ns.level_map(np.digitize(S[cut:], np.quantile(S[cut:], np.linspace(0, 1, 11)[1:-1])), S[cut:])
    ceil_lv = np.digitize(S[:cut], np.quantile(S[cut:], np.linspace(0, 1, 11)[1:-1]))
    ceil = ns.kl_recovery(model, moves[:n_sim], lengths[:n_sim], a.unit, key, ns.apply_level_map(ceil_m, ceil_lv), S[:cut])
    share = sim["recovery"] / ceil["recovery"] if ceil["recovery"] > 0 else float("nan")
    rec_ = {"call": used + 1, "time": time.strftime("%Y-%m-%dT%H:%M:%S"), "f1": f1, "precision": prec, "recall": rec, "auroc": au,
            "sim_recovery": sim["recovery"], "ceiling_recovery": ceil["recovery"], "sim_share_of_ceiling": share, "program": code}
    with open(work_dir(a.unit) / "dev_calls.jsonl", "a") as f:
        f.write(json.dumps(rec_) + "\n")
    print(f"{a.unit} dev call {used + 1}/{NC['max_dev_calls']} ({time.time() - t0:.0f}s)")
    print(f"  detection: F1 {f1:.3f} (precision {prec:.3f}, recall {rec:.3f}), AUROC {au:.3f}; "
          f"unit fires on {fire[el].mean():.1%} of scored positions, program on {pred[el].mean():.1%}")
    print(f"  simulation: recovers {sim['recovery']:.1%} of the zero-ablation damage; a perfect 10-level reader recovers "
          f"{ceil['recovery']:.1%}; share of ceiling {share:.2f}")
    rng = np.random.default_rng(used)
    for name, sel in (("FALSE POSITIVES (program says fires, unit does not)", pred & ~fire), ("MISSES (unit fires, program does not)", fire & ~pred)):
        idx = np.flatnonzero(sel)
        print(f"\n--- {name}: {len(idx)} positions; examples ---")
        for i in rng.choice(idx, min(a.show, len(idx)), replace=False) if len(idx) else []:
            b = bs.board(int(i))
            print(f"[pos {i}] pole act {st[a.unit]['sign'] * S[i]:.3f}, program {pred_v[i]:.2f}, moves {','.join(map(str, b.moves))}")
            show(b)


def cmd_synth(a):
    units, us, key, st = ctx()
    mv = parse_moves(a.moves)
    model = ns.load_web_model()
    v = st[a.unit]["sign"] * ns.acts_for_sequence(model, mv, a.unit, key)[-1]
    best = st[a.unit]["dev_max_pole"]
    bad = legal_game_error(mv)
    if bad:
        print(f"{a.unit}: pole activation {v:.3f}, but this sequence does not count: {bad}")
        return
    print(f"{a.unit}: pole activation {v:.3f}; dev maximum {best:.3f} -> {'BEATS the dev maximum' if v > best else 'below the dev maximum'}")


REQUIRED = {"unit": str, "description": str, "program": str, "synthesis": list, "confidence": str}


def cmd_submit(a):
    units, us, key, st = ctx()
    d = json.load(open(a.file))
    for k, t in REQUIRED.items():
        if not isinstance(d.get(k), t):
            sys.exit(f"field '{k}' missing or not {t.__name__}")
    if d["unit"] != a.unit:
        sys.exit("unit field does not match")
    if d["confidence"] not in ("high", "medium", "low"):
        sys.exit("confidence must be high, medium or low")
    if len(d["description"].split()) > 80:
        sys.exit("description must be at most 80 words")
    if len(d["synthesis"]) > 5:
        sys.exit("at most 5 synthesis sequences")
    for s in d["synthesis"]:
        bad = legal_game_error(parse_moves(",".join(map(str, s))))
        if bad:
            sys.exit(f"synthesis sequence {s} is not allowed: {bad}")
    fires_fn, level_fn = ns.load_program(d["program"])
    moves, _, lengths = dev_data()
    bs = ns.BoardSet(moves[:20], lengths[:20])
    ns.run_program(fires_fn, bs)
    if level_fn:
        ns.run_program(level_fn, bs)
    d["dev_calls_used"] = calls_used(a.unit)
    d["submitted"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    out = ns.NS / "descriptions"
    out.mkdir(exist_ok=True)
    (out / f"{a.unit}.json").write_text(json.dumps(d, indent=1))
    print(f"{a.unit}: stored {out / (a.unit + '.json')}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("units")
    x = sp.add_parser("examples"); x.add_argument("unit"); x.add_argument("--n", type=int, default=40); x.add_argument("--band", type=int); x.add_argument("--seed", type=int, default=0)
    x = sp.add_parser("act"); x.add_argument("unit"); x.add_argument("--moves", default="")
    x = sp.add_parser("facts"); x.add_argument("--moves", default="")
    x = sp.add_parser("steer"); x.add_argument("unit"); x.add_argument("--moves", default=""); x.add_argument("--to", default="max")
    x = sp.add_parser("score"); x.add_argument("unit"); x.add_argument("program"); x.add_argument("--show", type=int, default=4)
    x = sp.add_parser("synth"); x.add_argument("unit"); x.add_argument("--moves", default="")
    x = sp.add_parser("submit"); x.add_argument("unit"); x.add_argument("file")
    a = p.parse_args()
    {"units": cmd_units, "examples": cmd_examples, "act": cmd_act, "facts": cmd_facts, "steer": cmd_steer, "score": cmd_score,
     "synth": cmd_synth, "submit": cmd_submit}[a.cmd](a)


if __name__ == "__main__":
    main()
