# Neuron Scientist: agent-written, verified neuron descriptions

This is the protocol for describing units of the Connect Four model with an AI agent and checking those descriptions on
held-out data. It follows Goodfire's "Neurons as an Interpretable Basis" (Tigges et al. 2026), where a frontier model ran
experiments on each neuron, revised its description against a dev metric, and was then scored on held-out data by
detection, simulation and input synthesis. Connect Four lets us go one step further: every description is written twice,
in English and as a short program over the board, so detection is scored exactly instead of by a judge. Pre-registration:
`docs/PLAN.md`, addendum (q).

## What runs where

| Step | Who runs it | Command | Reads |
|---|---|---|---|
| 0. Setup | you | `uv sync`, `uv run pytest -q tests/test_ns.py` | - |
| 1. Prepare | you (once) | `uv run python scripts/30_ns_prepare.py` | dev split, neuron table |
| 2. Describe | the agent session | `uv run python scripts/31_ns_tool.py ...` | dev split only |
| 3. Verify | you, after every unit is submitted | `uv run python scripts/32_ns_verify.py run` | test split |
| 4. Text-only judge | fresh subagents, one per unit | `32_ns_verify.py judge-export`, then `judge-score` | `ns/judge/<unit>.json` only |

Everything runs on CPU; no GPU is needed. Rough cost: prepare 3-5 min; each dev-metric call 15-40 s; verification 30-60 min
for 70 units (it computes concept labels for 10,000 games and runs simulations). Tokens: roughly 50-100k per unit for the
describing agent, so 70 units is several million tokens. Run on a machine you do not mind keeping busy (a cloud sandbox is
ideal).

The 70 units are: 20 neuron poles that the fixed concept dictionary already explains, 40 that it does not, and 10 random
directions in a layer's neuron space (blinded controls). Unit ids are shuffled, and nothing the agent can read says which is
which. Verification unblinds them.

## Rules that keep the result valid

1. The describing agent and its subagents never open `ns/private/`, `ns/cache/test_acts.npy`, `data/val.npz`,
   `results/pole_table.json`, `results/concept_coverage.json`, `results/*concept*`, or `docs/LOG.md`, and never run
   `32_ns_verify.py`. These hold the unblinding key, the test data, or our earlier labels for these neurons.
2. At most 8 calls to `score` per unit (the tool enforces it). `examples`, `act`, `facts`, `steer` and `synth` are unlimited.
3. Do not edit `c4n/ns.py`, the scripts or the config. If a tool is broken, stop and report it.
4. Verification runs once, after every unit is submitted. Do not revise descriptions after seeing the report.
5. Saying "no clear concept" (confidence `low`) is a valid, useful answer. Some units are random directions; inventing a story
   for them is the failure this study is designed to catch.

## The Board API (what a program sees)

A program is plain Python that defines `fires(b)` returning `True/False` (or a number in 0-1), and optionally `level(b)`
returning an integer 0-9 for how strongly the unit is active (used for the simulation score; it defaults to `fires`). No
imports, no file access, no names with double underscores; the words `import`, `open(`, `exec(`, `eval(` may not appear
anywhere in the code, including comments. Available builtins: `abs all any bool dict enumerate float int len list max min
range round set sorted sum tuple zip reversed`.

The board is seen by the player **about to move** ("me"):

| Field | Meaning |
|---|---|
| `b.grid[r][c]` | 0 empty, 1 mine, 2 theirs. Row 0 is the bottom, column 0 the leftmost (columns 0-6). |
| `b.heights[c]` | stones in column c |
| `b.landing(c)` | row where a stone dropped in column c would land, or `None` if full |
| `b.legal` | playable columns |
| `b.last_col`, `b.last_row` | where the last stone went (`None` at the start); that stone is the opponent's |
| `b.ply` | stones on the board; `b.me_first` is True if "me" is the first player |
| `b.my_wins`, `b.their_wins` | sets of empty `(r, c)` cells that would complete four for me / them |
| `b.my_playable_wins`, `b.their_playable_wins` | the subset that are landing cells now (an immediate win / a must-block) |
| `b.moves` | the game so far, as a list of columns |

Example:

```python
def fires(b):
    # the opponent just played in column 3 and now has three stacked there with the cell above empty
    c = b.last_col
    if c != 3 or b.heights[3] < 3:
        return False
    top = b.heights[3] - 1
    return all(b.grid[top - k][3] == 2 for k in range(3)) and b.landing(3) is not None

def level(b):
    return 9 if fires(b) else (3 if b.last_col == 3 else 0)
```

## The final submission (one JSON file per unit)

```json
{
  "unit": "U07",
  "description": "One to three sentences, at most 80 words: exactly when the unit fires, in board terms a Connect Four player would understand. Mention what does NOT make it fire if that matters.",
  "effect": "What the unit does to the model's move when it is strongly active (from steer), e.g. 'raises column 3 by about 10 points'; or 'none measurable'.",
  "program": "def fires(b):\n    ...\n\ndef level(b):\n    ...\n",
  "synthesis": [[3, 3, 4, 2], [3, 3, 4, 4, 2]],
  "confidence": "high | medium | low",
  "notes": "Short lab notes: hypotheses tried, what the dev metric said, open doubts."
}
```

`synthesis` holds up to 5 legal move sequences that you built to make the unit fire as strongly as possible; the goal is to
beat its dev maximum (`synth` tells you). Store it with `uv run python scripts/31_ns_tool.py submit U07 path/to/final.json`.

---

## PROMPT FOR THE ORCHESTRATING SESSION (paste this)

> You are running a pre-registered interpretability study in the repository `connect4-neurons` (already cloned; you are in its
> root). Read `docs/NEURON_SCIENTIST.md` fully before doing anything, then follow it exactly. Your job is to coordinate the
> description of 70 units of a small transformer that plays Connect Four, by running one "Neuron Scientist" subagent per unit,
> and to keep the study valid.
>
> 1. Setup: run `uv sync`, then `uv run pytest -q tests/test_ns.py` (must pass). If `ns/units.json` does not exist, run
>    `uv run python scripts/30_ns_prepare.py`. Do not print or open anything in `ns/private/`.
> 2. Run `uv run python scripts/31_ns_tool.py units` to list the units.
> 3. For each unit, start a subagent with the "PROMPT FOR ONE UNIT" from `docs/NEURON_SCIENTIST.md`, with `{UNIT}` replaced by
>    the unit id. Run several at once if you can (they do not share state; each writes only `ns/work/{UNIT}/` and its own
>    submission). Do a pilot first: three units, then read their notebooks and submissions and check they follow the rules
>    (budget, program sandbox, honest confidence). Fix only your instructions, never the code, then run the rest.
> 4. Check that every unit has `ns/descriptions/{UNIT}.json` (`31_ns_tool.py units` shows "submitted"). For any unit whose
>    subagent failed, rerun it once.
> 5. Freeze: `git add ns/descriptions ns/work ns/units.json ns/stats.json && git commit -m "Neuron Scientist: frozen descriptions"`.
> 6. Verify (once): `uv run python scripts/32_ns_verify.py run`. Then `uv run python scripts/32_ns_verify.py judge-export`.
> 7. Text-only judge: for each unit, start a FRESH subagent with the "PROMPT FOR THE JUDGE" below and `{UNIT}` filled in. It
>    may read only `ns/judge/{UNIT}.json` and must write `ns/judge_answers/{UNIT}.json`. It must not run any command or read
>    any other file. Then run `uv run python scripts/32_ns_verify.py judge-score`.
> 8. Commit `ns/report.json`, `ns/report.md`, `ns/judge`, `ns/judge_answers` and push. Reply with the summary table from
>    `ns/report.md`, which predictions held, and anything that went wrong. Do not reinterpret or soften the results.
>
> Never open the forbidden files listed in the rules, never edit the analysis code, and never revise a description after step 6.

## PROMPT FOR ONE UNIT (the orchestrator fills in `{UNIT}`)

> You are a Neuron Scientist. Your subject is unit `{UNIT}` of a 6-layer transformer (d_model 256, 1,024 MLP neurons per layer)
> that plays Connect Four. The model reads the game as a sequence of column numbers (0-6) and predicts the next move; it was
> trained to imitate a depth-10 search engine and agrees with it on 94% of positions. A unit is one direction in the MLP
> activation space of one layer, with a sign (a "pole"); it **fires** when its pole activation exceeds its own 97th
> percentile on the dev games. Some units may be random directions with no clean meaning; you are not told which.
>
> Goal: find the most accurate, simple description of when `{UNIT}` fires, written twice: in plain English and as a program
> `fires(b)` (plus optional `level(b)` 0-9) over the Board API in `docs/NEURON_SCIENTIST.md` (read the "Board API" and
> "final submission" sections first). Then find what it does to the move, and build positions that drive it as high as
> possible.
>
> Tools (all read only the dev games; run from the repository root):
> - `uv run python scripts/31_ns_tool.py examples {UNIT} --n 40` (and `--band 9 --n 10` for the very top, `--band 5` around the
>   firing threshold, `--seed k` for fresh samples): positions across activation bands, with boards, moves and tactical facts.
> - `... act {UNIT} --moves 3,3,4,2`: the unit's activation after each move of a game you write. Use it to test a hypothesis by
>   editing a position one stone at a time (minimal pairs) and watching the activation.
> - `... facts --moves ...`: board, landing cells, immediate wins and must-blocks, threat cells, engine scores.
> - `... steer {UNIT} --moves ... --to max|zero`: how the move probabilities change when the unit is forced high or off.
> - `... synth {UNIT} --moves ...`: does a position beat the unit's dev maximum?
> - `... score {UNIT} program.py`: THE DEV METRIC, at most 8 calls. It reports detection F1, precision, recall and AUROC of
>   your program against actual firing, how much of the unit's effect your `level` recovers when it replaces the unit
>   (simulation, as a share of a perfect 10-level reader), and examples of false positives and misses. Spend these calls on
>   genuinely different hypotheses or fixes; do the cheap tests with `act` first.
>
> Method: (1) Look at 40+ examples across bands; write 2-3 candidate hypotheses in `ns/work/{UNIT}/notebook.md`. (2) Test each
> with minimal pairs via `act` before scoring. (3) Score the best, read the false positives and misses, refine. (4) Prefer a
> simple description that covers most firing over a complicated one that overfits; note exceptions in words. (5) Use `steer`
> on 3+ positions to describe the effect. (6) Build up to 5 synthesis positions and check them with `synth`. (7) Write
> `ns/work/{UNIT}/final.json` and run `... submit {UNIT} ns/work/{UNIT}/final.json`.
>
> Keep `ns/work/{UNIT}/notebook.md` as a lab notebook: hypotheses, tests, the dev metric after each `score` call, and why you
> changed course. Confidence: `high` if your best dev F1 >= 0.7 and the minimal-pair tests agree; `medium` if F1 is 0.4-0.7
> or there are clear exceptions; `low` if nothing exceeds 0.4 or the unit looks like a mixture. A `low` with an honest
> description is better than a confident story.
>
> Rules: read only `docs/NEURON_SCIENTIST.md`, `c4n/ns.py` (to understand the Board), and your own `ns/work/{UNIT}/`. Never
> open `ns/private/`, `ns/cache/`, `data/val.npz`, `results/`, `docs/LOG.md` or `docs/PLAN.md`, and never run
> `32_ns_verify.py`. Do not edit any code. Do not look at other units' work. When you are done, reply with your final
> description, its best dev F1, the simulation share, and your confidence.

## PROMPT FOR THE JUDGE (a fresh subagent per unit)

> You are judging one description of a unit in a Connect Four model. Read only `ns/judge/{UNIT}.json`. It holds a
> `description` of when the unit fires and a list of `pairs`. In each pair, exactly one of the two positions (A or B) makes the
> unit fire. Boards are drawn from the point of view of the player about to move (X = that player, O = the opponent; row 0 is
> the bottom line printed last; columns 0-6). Using only the description, decide for each pair which position fires. Write
> `ns/judge_answers/{UNIT}.json` as `{"answers": ["A", "B", ...]}`, one answer per pair, in order. Do not open any other file,
> do not run any command, and do not guess from anything but the description and the boards. Reply "done" when written.

## What comes back

`ns/report.md` lists every unit unblinded: kind (neuron or random direction), stratum, layer and neuron, held-out detection F1
and AUROC of the program, the dictionary baseline and its concept, simulation share of ceiling, input synthesis, the measured
steering effect, the agent's confidence and description. Its header evaluates predictions (q-a) to (q-e). The descriptions
can then be shown in the neuron atlas next to each neuron, with their verified scores.
