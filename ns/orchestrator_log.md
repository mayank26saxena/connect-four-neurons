# Orchestrator log (Neuron Scientist run, 2026-11-21)

## Environment
- Run on a Mac (Apple Silicon, 18 cores, CPU) from `connect4-neurons-main.zip` (upstream e9bc7f2). The zip had no git
  history, so a local baseline commit was made before the run; pushing from this machine is not possible.
- `uv sync` OK; `tests/test_ns.py` 4 passed; `30_ns_prepare.py`: 70 units, 171,788 dev positions cached.

## Instruction changes to the per-unit prompt (code untouched)
- Pilot (U01-U03): protocol text verbatim, plus a preamble giving the absolute repo path, "cd there first" (the shell
  resets its directory), and "create ns/work/{UNIT}/; write program files only there".
- After the pilot, approved by the study owner: added "use one common measurement: do not build your own scorer, F1
  evaluator or trained classifier from tool output; `score` is the only measure of program quality; simple counts and
  histograms are fine" and "check synthesis positions with `synth`".

## Deviations
- U03 (pilot): built a local F1 evaluator over ~1,860 dev positions scraped from `examples` output and trained a
  gradient-boosted classifier as a ceiling check; used 4/8 `score` calls. Dev data only; no forbidden file accessed.
  Initially kept as submitted; later superseded by a rerun (see "Pilot reruns" below).
- U02 (pilot): had started a similar local evaluator (ev.py, dev_boards.pkl) before the clarification was sent mid-run
  at 4/8 `score` calls; told to stop using it and record what it did in its notebook.
- U01 (pilot): followed the method by hand (7/8 `score`); synthesis positions checked with `act` rather than `synth`
  (same dev-max comparison).

## Pilot reruns (decided by the study owner before any verification)
- U02 pilot stopped mid-run (4/8 `score`, had built local evaluators and tree/boosting fits: ev.py, gbm.py, tree*.py).
- U02 and U03 pilot work moved untouched to `ns/superseded/U0{2,3}_pilot1/` (U03's submission kept there as
  `submitted_description.json`). Nothing deleted. Budgets reset by moving the work dirs.
- Both units rerun from scratch by fresh subagents under the common-measurement prompt, which also forbids reading
  `ns/superseded/`. The rerun submissions are the official ones, whatever they score. No further reruns except for
  a subagent that fails outright (protocol step 4).
- Template for all remaining units: the same prompt (`ns/prompts/unit_prompt_v2.txt`; pilot prompt in `unit_prompt_v1_pilot.txt`). From U04 on, each subagent is told to read that file with {UNIT} substituted.

## Per-unit audits (tool inputs scanned for forbidden paths and homemade scoring/ML; budget from dev_calls.jsonl)
- U01 (pilot v1 prompt): clean, 7/8, high.
- U05: clean, 3/8, high. Note: `score` reported a negative perfect-reader ceiling (-75.1%), so simulation share is NaN
  for this unit (tool behaviour, not an agent error). Activations are tiny (dev max 0.012).
- U06: clean, 6/8 (one call repeated after truncated output), medium (F1 0.436).
- U02 (rerun, v2): clean, 4/8, low (F1 0.644 but described as mixture; within rubric). Helpers are counts/histograms over act on random games and an act-guided synthesis search; no local scorer.
- U04: clean, 7/8 (one call wasted: piping re-ran the scorer), high (F1 0.705 best / 0.701 submitted). Note: 2 units so far lost a call to output handling; prompt left unchanged mid-run to keep one version.
- U10: clean, 6/8 (one repeat after truncated output), low (F1 0.25). Note: `synth`/`act` accepted move lists containing a completed four (game over); agent excluded those from its synthesis. Tool behaviour to check before verification.

## Synthesis legality check (added by orchestrator; code untouched)
- `parse_moves` in 31_ns_tool.py checks only column capacity, so a synthesis sequence can pass through a finished game
  (a move completing four), although the protocol asks for legal move sequences.
- Audit now replays every submitted synthesis sequence and flags any move that completes a four for either side.
- U04: all 5 sequences flagged (fours completed at move 15 or 21 while filling columns). Agent resumed and asked to
  replace only the `synthesis` field with game-legal sequences, no extra `score` calls, and resubmit (pre-verification).
- Rule applied to every unit the same way: flagged units are resumed with the same request. Prompt v2 left unchanged.
- U03 (rerun, v2): clean, 7/8 (one duplicate call), low (F1 0.225; pilot attempt had 0.226). Synthesis legal; best 9.34 < dev max 12.22 (pilot had beaten it via a bottom-row winning setup).
- U11: clean, 5/8, medium (F1 0.415, precision 0.93). Simulation share negative (-0.17). 1 of 5 synthesis sequences completed a four at move 18/19; agent resumed for the legality fix.
- U13: clean, 3/8, medium (F1 0.452, precision 0.975, sim 0.84). Agent itself excluded game-over sequences.
- U11 legality fix done: 1 sequence replaced (no four), still 5/8 score calls; re-audit clean.
- U08: clean on paths, 7/8 (one accidental repeat), medium (F1 0.507). Self-reported: saved ~1,200 example positions to /tmp and tallied firing counts by 3 features, then deleted it; counts are allowed, no candidate rule was scored locally. Accepted, flagged.
- U07: clean on paths, 7 logged score calls (agent reported 8 incl. 2 accidental reruns), medium (F1 0.445). 2 of 5 synthesis sequences completed a four (incl. its only beats-max one); resumed for legality fix.
- U04 legality fix done: 5 new legal sequences (2 beat dev max at 6.014/6.012), still 7/8; re-audit clean.
- U07 legality fix done: 2 sequences replaced (both legal, beat dev max 8.07/8.01); re-audit clean.
- U16: clean, 7/8 (one accidental repeat), high (F1 0.842, sim 1.05). Synthesis legal, none beats max.
- U14: clean, 5/8, low (F1 0.130). Synthesis legal, 3 beat max.
- U12: clean, 4/8, low (F1 0.169). Synthesis legal, none beats max.
- U09: clean, 7/8 (one accidental repeat), low (F1 0.206). Synthesis legal, all 5 beat max (best 21.5 vs 14.6).
- U15: clean, 7/8, low (F1 0.179). Synthesis legal, 2 beat max.
- U21: clean, 7/8 (one accidental repeat), low (F1 0.208). Synthesis legal, 1 beats max.
- U18: clean, 4/8, low (F1 0.152). Helpers compute feature means per examples file (counts, no F1). Synthesis legal, none beats max.
- U17: clean, 6/8, low (F1 0.363). Synthesis legal, 4 beat max.
- U19: clean, 6/8, low (F1 0.225). Self-reported temporary /tmp counts from examples (counts only, deleted). Synthesis legal, 4 beat max.
- U25: clean, 8/8 (one accidental repeat), medium (F1 0.539). Program embeds an exact endgame solver (<=16 empty cells, <=3 legal columns); sandbox-compliant but may slow verification. Synthesis legal, none beats max.
- U24: clean, 8/8, medium (F1 0.545, sim 0.48). Move-order dependent. Synthesis legal, 1 beats max.
- U20: clean, 4/8, low (F1 0.164, sim -0.08). Synthesis legal, all 5 beat max.
- U27: clean, 8/8 (two accidental reruns), medium (F1 0.628). Synthesis legal, 1 beats max.
- U22: clean, 5/8, low (F1 0.409 from a ply-3 opening lookup table built by exhaustive `act`; agent chose low because it is a table, not a concept). Synthesis legal, none beats max. Flag: lookup-table programs (U02/U05/U17/U22 use opening enumeration) can score well on detection without being a concept; consider in analysis.
- U28: clean, 7/8 (one accidental repeat), medium (F1 0.448, sim 0.82). Synthesis legal, 2 beat max.
- U30: clean, 7/8 (one accidental repeat), medium (F1 0.596, sim 0.73). Synthesis legal, 4 beat max.
- U29: clean on paths, 6/8 (one repeat after piping), medium (F1 0.702, sim 0.61). 4 of 5 synthesis sequences complete a four (2 on the final move, 2 at move 7); resumed for legality fix. Rule clarified to agents: no move, including the last, may complete a four.
- U23: clean, 5/8 (one accidental repeat), low (F1 0.224). Synthesis legal (agent excluded a post-four position itself), none beats max.
- U26: clean, 5/8, low (F1 0.180). Synthesis legal, none beats max.
- U29 legality fix done: 4 sequences replaced; all 5 legal and beat max (best 2.92, down from 3.18). Diff vs pre-fix snapshot: only synthesis/notes/submitted changed. Still 6/8.
- U36: clean, 1/8, high (F1 0.986 for `ply == 0`: empty-board detector; sim 0.01). Agent flagged it may be a random direction picking up a start-of-sequence signal.
- U31: clean, 7/8 (one accidental repeat), low (F1 0.397; includes a 13-opening lookup). Synthesis legal, 4 beat max.

## Observation for analysis (orchestrator, pre-verification)
- Several units are opening/ply detectors (U02 ply 1, U05 ply 1, U17 ply 3, U22 ply-3 table, U36 ply 0). Every dev game shares the
  same first positions, and one ply is ~1/40 of positions, close to the 3% firing rate. So any direction (including a random one)
  whose value on a fixed early position happens to be extreme can "fire" there and get a near-perfect, trivially exact program
  with "high" confidence. Predictions about random controls being marked low should be read with this in mind; check in the report
  how many random-direction units are ply detectors.
- U33: clean, 6/8 (one accidental repeat), low (F1 0.306). Synthesis legal, all 5 beat max.
- U32: clean on paths, 6/8 (one accidental repeat), medium (F1 0.466). BORDERLINE: /tmp/u32s/conj.py parsed ~examples output and counted, per activation band, how often 7 named candidate rules hold (A, B, A&B, A|B, shifted variants). That is closer to local rule evaluation than a plain histogram, though no F1/precision was computed and nothing was fitted. Kept; flagged for the study owner's decision (rerun or accept).
- U41: clean, 3/8, high (F1 1.000 for `ply == 0`; empty-board detector #2; sim 0.22). Synthesis = empty board, equal to dev max. Note: agent reports `synth` labels a tie as beating; 32_ns_verify.py uses strict > (line 92), so ties will not count.
- U35: clean on paths, 7/8, low (F1 0.369; tiny activation range, dev max 0.006). Self-reported: a helper (gen.py, random games, no dev data) was briefly written outside ns/work/U35/ then moved in; git status shows no stray files outside ns/. Synthesis legal, none beats max.
- U37: clean, 6/8 (one rerun), medium (F1 0.601, sim 0.54). Synthesis legal, none beats max.
- U38: clean, 7/8, medium (F1 0.679, sim 0.32). Synthesis legal, all 5 beat max.
- U34: clean, 8/8 (one accidental repeat), medium (F1 0.695, sim 0.51). Tactical unit: column 5 empty and (1,5) bad for me; suppresses column 5 under steering. Synthesis legal, none beats max.
- U42: clean, 6/8 (call 1 output truncated), high (F1 0.720, sim 0.99). Synthesis legal, 4 beat max.
- U46: clean, 8/8, medium (F1 0.597, sim 0.25). Synthesis legal, 2 beat max.
- U39: clean, 6/8 (one accidental repeat), low (F1 0.33). Agent notes a mislabel in its own final.json notes (attributes 0.33 to p4; it came from p3); notes are not scored, left as is. Synthesis legal, 2 beat max.
- U43: clean, 7/8, medium (F1 0.657, sim 0.83). Synthesis legal, none beats max.
- U48: clean, 6/8, medium (F1 0.643; opening detector ply 1 col 5/3/4 plus column-4 filling). Synthesis legal, none beats max (dev max is the ply-1 opening).
- U44: clean, 6/8, low (F1 0.119). Synthesis legal, 4 beat max.
- U47: clean, 6/8, medium (F1 0.514, sim 0.91). Helpers are counts over examples output and an act-only hill climb. Synthesis legal, 3 beat max.
- U45: clean on paths, 7/8 (one accidental repeat), low (F1 0.340). Helpers (frac*.py, rough.py) compute, per activation-band file,
  the fraction of positions where named candidate features hold. Same pattern as U32.
- Interpretation applied uniformly: per-band frequencies of a feature (including named candidate features) count as the
  "simple counts" the rule allows, as long as no F1/precision/recall is computed and nothing is fitted. U32 and U45 are the
  clearest cases; a pre-freeze scan of all helper scripts will list every unit that did this so the owner can decide.
- U40: clean on paths, 5/8, low (F1 0.480). 2 of 5 synthesis sequences complete a four at move 29/30 (hill-climb lines); resumed for legality fix.
- U49: clean, 7/8, low (F1 0.227). Synthesis legal, 1 beats max.
- U53: clean, 4/8, medium (F1 0.670, sim 0.75). Synthesis legal, 1 beats max.
- U52: clean, 5/8, low (F1 0.284). Synthesis legal, 2 beat max.
- U50: clean, 6/8 (one accidental repeat), medium (F1 0.735, chose medium over high because the rule is a hand-weighted opening tally). Synthesis legal, 2 beat max.
- U40 legality fix done: 2 sequences replaced; diff vs snapshot only synthesis/notes/submitted; still 5/8; best now 4.615 < max.
- U56: clean, 7/8 (one accidental repeat), medium (F1 0.528). Simulation share NaN (negative ceiling, as U05). Strong causal effect: max steer moves ~95% of probability to column 6. Synthesis legal, none beats max.
- U57: clean, 4/8, medium (F1 0.441). Simulation share NaN (negative ceiling). Must-block in column 1; steering pushes column 1. Synthesis legal, 3 beat max.
- U51: clean, 3/8, medium (F1 0.720 for a ply-1 opening rule; chose medium over high due to unexplained ~44% mid-game firing). Opening detector #7. Synthesis legal, 1 beats max. Agent stopped with background work still running; recheck against snapshot at freeze.
- U64: clean, 2/8, high (F1 0.985 for `ply == 0`; empty-board detector #3; sim 0.01). Synthesis = empty board tie, none beats max.
- U60: clean on paths, 8/8 (one accidental rerun), medium (F1 0.663). 4 of 5 synthesis sequences complete a four (column-filling lines); resumed for legality fix.
- U59: clean, 4/8, medium (F1 0.837 for a ply-1 opening rule; opening detector #9). Synthesis legal, none beats max.
- U60 legality fix done: 4 sequences replaced (generated in /tmp, checked with synth); diff vs snapshot only synthesis/notes/submitted; none beats max now (2.939 < 2.976).
- U54: clean, 4/8 (one repeat after truncated output), low (F1 0.207). Synthesis legal (3 sequences), none beats max.
- U62: clean, 7/8 (one repeat after truncated output), medium (F1 0.511). Layer-0 move-token mix; helper rand.py runs act on random games. Synthesis legal, none beats max.
- U63: clean on paths, 2/8, medium (F1 0.593 for a ply-1 opening rule; opening detector #11; sim share 4.18 > ceiling, tool quirk). 2 of 5 synthesis sequences contain a vertical four at move 7; resumed for legality fix.
- U63 legality fix done: 2 sequences replaced; replay check clean; diff only synthesis/notes/submitted; still 2/8.
- U55: clean, 7/8, low (F1 0.255). Weights from counts of firing vs non-firing examples (no fit). Synthesis legal, all 5 beat max.
- U58: clean, 6/8, low (F1 0.167). Cell weights from firing/non-firing fill counts (agent self-flagged). Synthesis legal, 2 beat max.
- U70: clean, 4/8 (one rerun to read cut-off output), high (F1 0.886, sim 1.07). Closely parallels U01 (centre column stack, top stone theirs; U01 height 4, U70 height 3). Synthesis legal, none beats max.
- U66: clean, 7/8 (one accidental repeat), low (F1 0.145). Synthesis legal, all 5 beat max.
- U61: clean, 6/8, medium (F1 0.440). Synthesis legal, 1 beats max.
- U69: clean, 5/8 (one accidental double run), medium (F1 0.649, sim 0.47). Program embeds an exact endgame solver (<=16 empty), like U25. Synthesis legal, all 5 beat max.
- U67: clean on paths, 7/8, low (F1 0.194). Saved ~5,400 lines of examples output (ex300*.txt) and computed per-cell fill frequencies by band (counts; no rule scoring). Same category as U32/U45/U58 for the owner's review. Synthesis legal, 4 beat max.
- U65: clean, 6/8 (one accidental duplicate), low (F1 0.205). Synthesis legal, 1 beats max.
- U68: clean on paths, 5/8, low (F1 0.237). Helpers count features over example boards. Synthesis legal, 4 beat max.

## All 70 submitted (pre-freeze)
- Full re-audit of all 70: no forbidden-path access, no ML/scorer keywords, all synthesis legal, all within 8 score calls; every submission matches its post-audit snapshot.
- Helper-script classification (A plain / B counts / C named-rule band counts / D local scoring or fitting) delegated to a read-only agent; results go to the study owner before freeze.

## Helper-script classification (read-only agent, pre-freeze)
- No unit used sklearn/numpy fitting/regression; no helper computed F1/precision/accuracy/tp-fp-fn. All F1 figures in notebooks come from `score`.
- D (borderline C/D): U68 (count2.py prints recall/"cover" of a candidate disjunction on saved firing boards; count4.py ranks cell pairs by lift).
- C: U09, U33, U39, U45, U66, U69 (borderline D: population-reweighted fire/non-fire masses per candidate cell), U19 and U20 (borderline B),
  plus U32 (orchestrator correction: its named-rule script was in /tmp/u32s/conj.py, outside ns/work, so the agent auditor missed it).
- B: most other units (plain counts/histograms); A: the rest. U08 and U19 also counted over /tmp dumps they deleted.
- Decision on reruns: pending the study owner.
- Study owner decision (pre-freeze): rerun U68 and the 9 C units (U09, U19, U20, U32, U33, U39, U45, U66, U69) from scratch.
  Old work moved untouched to ns/superseded/UXX_v2/ (U32's /tmp/u32s moved there too). Budgets reset.
- Reruns use ns/prompts/unit_prompt_v3_reruns.txt: identical to v2 except the common-measurement sentence now states explicitly that
  counting how often a candidate rule holds among firing vs non-firing examples is not allowed (plain single-feature histograms are).
  This makes v2's intent explicit; the other 60 units were audited as A/B under the same line. Rerun results are final.
- U45 (rerun v3): clean, 7/8 logged (agent reports one piped double run), low (F1 0.291 submitted, best 0.301). Helpers: none beyond programs. Synthesis legal, 2 beat max. (v2: low, F1 0.340.)
- U69 (rerun v3): clean, 8/8 (two accidental reruns), medium (F1 0.481, sim -0.79). Solver gated to ply>=26 and <=3 legal columns. No helper scripts. Synthesis legal, none beats max. (v2: medium, F1 0.649.)
- U33 (rerun v3): clean, 7/8 (one accidental rescore), low (F1 0.344). Inline single-feature histograms only (last-move column, ply, cell occupancy by band), allowed under v3; two small awk helpers written to /tmp (minor deviation from 'write only in ns/work'). Synthesis legal, all 5 beat max. (v2: low, F1 0.306.)
- U32 (rerun v3): clean, 7/8 (one accidental repeat), medium (F1 0.517, sim 0.43). Helpers: hist.py/hh.py/enr.py single-cell and single-feature frequencies by band; probe.py runs its own program on hand-given sequences. Allowed under v3. Synthesis legal, all 5 beat max. (v2: medium, F1 0.466.)
- U09 (rerun v3): clean, 7/8 (one accidental repeat), low (F1 0.223). Inline single-feature histograms by band (column-4 height, per-cell occupancy, last move, teacher best move), allowed; one dump in /tmp/u09_moves.txt. Synthesis legal, all 5 beat max. (v2: low, F1 0.206.)
- U19 (rerun v3): clean, 8/8 (one accidental repeat), low (F1 0.259, sim 0.16). Helpers hist*.py: single-cell occupancy and column-height histograms firing vs non-firing over 560 saved examples; allowed. Synthesis legal, all 5 beat max. (v2: low, F1 0.225.)
- U68 (rerun v3): clean on paths, 6/8 (one accidental re-run), low (F1 0.243). Helpers: hist.py single-feature histograms (column counts, heights, last col); inline per-band counts of last column, parity, and whether the tool's 'must-block' fact is non-empty (/tmp dumps). The must-block count is a single tool-provided feature, so treated as allowed, but it is the closest any rerun came to the line (p1 was 'any must-block in col 0/2/4'). Synthesis legal, none beats max. (v2: low, F1 0.237.)
- U20 (rerun v3): clean, 5/8, low (F1 0.063, sim -0.09). Helpers: act wrapper and single-move-swap generator for synthesis. Synthesis legal, 2 beat max. (v2: low, F1 0.164.)
- U66 (rerun v3): clean, 7/8, low (F1 0.286, sim 0.12). hist*.py: single-feature histograms (stones by column parity, heights, column contents, ply, k-th last move). Allowed. Synthesis legal, 3 beat max. (v2: low, F1 0.145.)
- U39 (rerun v3): clean, 6/8 (one accidental repeat), low (F1 0.390). tally.py/htally.py: per-cell occupancy and per-column height/ply histograms fired vs not; allowed. Synthesis legal, 2 beat max. (v2: low, F1 0.331.)
- Frozen at commit 7d4de75 (sha256 of descriptions: e0c8afb2...). Verification started 2026-11-21 16:46.

## Text-only judge
- 70 fresh judges, prompt in ns/prompts/judge_prompt.txt. Audit: every judge made exactly one Read (its own ns/judge/UXX.json) and one Write (its own answers); no commands, no other files.
- 6 judges (U06, U25, U45, U54, U55, U68) wrote 19 answers for 20 pairs, so their answers cannot be aligned to pairs. Treated as failed subagents (protocol step 4): first answers moved to ns/superseded/judge_answers_first_try/, each rerun once with a fresh judge and the same prompt plus "there are exactly N pairs; write exactly N answers".
- Judge reruns: all 6 produced 20 answers; final audit of 70 judges clean (one Read of own pack, one Write of own answers each).
- judge-score: real mean 0.8275, random mean 0.84, q_e holds (criterion: real >= 0.80).

## Results notes (orchestrator, after verification; no reinterpretation of the pre-registered verdicts)
- q_d: report shows NaN because 3 real units (U56, U57, U63) have NaN simulation share (negative perfect-reader ceiling) and the
  median does not skip NaN. Excluding them the real-unit median is 0.119, still far below 0.5, so q_d fails either way.
- q_c: 3 of the 10 random directions are empty-board detectors (U36, U41, U64) rated "high" with test F1 ~1.0, as flagged before
  verification (opening-position artefact). Random median F1 0.58 > unexplained median 0.35.
- Synthesis "beats max" uses strict >; ties (empty-board or single-opening positions) do not count.
