# Study (s): orchestrator instructions

You coordinate a Neuron Scientist study on 50 blinded units (U01–U50) of a small Connect Four transformer. The protocol, tools,
prompt and rules are exactly those of the earlier study (r); only the units and the workspace (`ns3/`) are new.

## Setup (once)

1. Unpack the bundle and `cd connect4-neurons-s`. Call this folder `{REPO}` (its absolute path).
2. `uv sync`
3. Smoke check: `cd {REPO} && export C4N_CONFIG=ns3 NS_DIR={REPO}/ns3 && uv run python scripts/31_ns_tool.py examples U01 --n 2`
   It should print two positions. If it fails, stop and report the error; do not edit code.
4. Record in `ns3/orchestrator_log.md`: the date, the agent model you will use (use one model for every unit), and the sha256 of
   `ns3/prompts/unit_prompt_s.txt`.

## Running the units

- One fresh subagent per unit. Its prompt is `ns3/prompts/unit_prompt_s.txt` with `{UNIT}` replaced by the unit id and `{REPO}`
  by the absolute path. Add nothing else to the prompt: no hints, no guesses about what a unit might be.
- Pilot: U01–U03. Check that each followed the rules (at most 8 `score` calls, legal synthesis, only allowed files, no local rule
  counting, a `submit` at the end). Log what you checked. Change nothing unless a rule was broken; if you must change something, log
  it and why before launching more units.
- Then the rest in batches of about 10. After each unit, add one line to the log: unit, score calls used, confidence, best dev F1,
  any deviation.
- If a subagent breaks a rule, log it; do not delete or edit its submission. A unit may be re-run only if it crashed before
  `submit`, and the log must say so.

## What you must not do

- Do not open `ns3/private/` or `ns3/cache/`, and do not run any analysis of your own on the units.
- Do not read, compare, summarise or edit the descriptions beyond checking that `submit` succeeded.
- There is no verification step in this bundle (the held-out games are not included on purpose). Do not try to score the
  descriptions.

## Returning the results

Zip `ns3/descriptions/`, `ns3/work/` and `ns3/orchestrator_log.md` into `ns3_results.zip` and give it to the researcher, with a short
note: how many units were submitted, any re-runs or rule breaks, and the agent model used.
