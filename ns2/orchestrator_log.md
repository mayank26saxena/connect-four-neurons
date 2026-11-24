# Orchestrator log, study (r) (2026-11-21)

- Pre-registration: docs/PLAN.md addendum (r), committed with the code in eea45b4 before any (r) agent run.
- Config configs/ns2.yaml, workspace ns2/. Prepare: 90 units (20 explained, 40 unexplained, 30 random), 171,788 dev positions.
  Units and stats committed in 2142114; ns2/private (key) not opened by the orchestrator.
- One agent prompt for every unit: ns2/prompts/unit_prompt_r.txt (sha256 feff3980...).
- Pilot: U01-U03, then the rest in batches of about 10.
- U03 (pilot): clean, 6/8, low (F1 0.311). Stored in ns2/descriptions (the submit message prints a fixed 'ns/' path; cosmetic). Synthesis legal, 2 beat max.
- U02 (pilot): clean, 7/8, low (F1 0.257). Single-feature counts only (last-move cell by band). Synthesis legal, all 5 beat max.
- U01 (pilot): clean, 4/8, low (F1 0.227). Weights from single-cell band histograms + minimal pairs (allowed). Synthesis legal, 3 beat max.
- Pilot review: all three followed the rules (budget, legal synthesis, no forbidden files, no rule-counting). No prompt changes. Launching the rest.
- U08: 5/8, high (F1 0.748). Deviation: ran `ls -la` on ns/descriptions/U08.json (an (q) file, different unit) to check where its submission went, because `submit` printed a fixed "ns/descriptions/..." path. Metadata only, contents not read. Synthesis legal, all 5 beat max.
- Fix: `submit` now prints the real stored path (message text only; commit after 2142114). Agents already running may still see the old message.
- U04: clean, 6/8, low (F1 0.144). Synthesis legal, all 5 beat max.
  (U04 helpers: single-feature histograms by band; 'lambda' flags were defaultdict only.)
- U12: clean, 6/8, medium (F1 0.671, sim 1.64). 'I am winning' unit (immediate wins). Synthesis legal, 4 beat max.
- U07: clean, 6/8, low (F1 0.285). Synthesis legal, 1 beats max.
- U09: 5/8, low (F1 0.243). Synthesis legal, all 5 beat max.
- U11: clean, 5/8, low (F1 0.322). Helpers: per-cell occupancy histograms by band (relative and absolute colours). Synthesis legal, none beats max.
- U10: 6/8, low (F1 0.316). Synthesis legal, all 5 beat max.
- U13: 6/8, medium (F1 0.592; sim NaN). Layer-0 unit whose top band is entirely ply 6 (move-position effect, additive per-move contributions). Synthesis legal, 4 beat max.
- Observation (pre-verification): min_ply removes the fixed opening positions, but ply-specific (position-index) effects remain: a layer-0 direction can still fire at one exact ply (U13: ply 6) across many different boards. Unlike (q)'s empty-board case this is not one board, but random directions may show it too. Not changed mid-study; to check in the unblinded report.
- U05: 6/8, medium (F1 0.499, sim 0.58). Synthesis legal, 1 beats max.
  (U05 /tmp/u05hist.py: single-feature histograms within positions where column 4 has height 2; no rule hit rates. Accepted; helper written to /tmp, minor deviation. Agent stopped with background work; recheck snapshot at freeze.)
- U16: 5/8, high (F1 0.736, sim 0.71). Column-0 stack, opponent on top at row 3. Synthesis legal, none beats max.
- U17: 7/8, low (F1 0.236). Synthesis legal, all 5 beat max.
- U15: 8/8, medium (F1 0.507). Late-game left-edge-closed unit. Synthesis legal, 3 beat max.
  (U15 inline scripts: per-band histograms of open-column count, ply, per-column full% and mean height; single features, allowed. 300-example dump in /tmp.)
- U21: 5/8, low (F1 0.116). Synthesis legal, 1 beats max.
  (U21 helpers: per-cell occupancy histograms by band; allowed. U05 agent stopped after confirming its submission is unchanged.)
- U19: 8/8, medium (F1 0.464, sim 0.55). Column-4 full, opponent on top, recency. Synthesis legal, 2 beat max.
- U14: 4/8, low (F1 0.195). Helpers single-feature histograms. Synthesis legal; best ties max (synth labels float-equal as beating; verify uses strict >).
- U18: 7/8, low (F1 0.130). Synthesis legal, 4 beat max.
- U06: 6/8, low (F1 0.432; chose low despite F1>0.4: additive layer-0 move tally, no board pattern). Sim NaN. Synthesis legal, all 5 beat max.
  (U06 calc2.py ranks its hand score against activations it measured with act on ~30 hand-built positions; act-based checking, not dev-position scoring. Allowed.)
- U22: 5/8, low (F1 0.337; sim NaN). Synthesis legal, all 5 beat max.
- U20: 8/8, medium (F1 0.493). Endgame unit. Synthesis legal, 1 beats max.
- U24: 6/8, low (F1 0.121). Synthesis legal, none beats max.
- U25: 5/8, low (F1 0.233, sim 0.67). Synthesis legal, 2 beat max (one ties).
- U23: 6/8, medium (F1 0.525). Program embeds a 10-ply forced-loss search, gated on column 5 full. Synthesis legal, none beats max.
- U30: 7/8, low (F1 0.371). Column-4-full unit; max steer cuts column 4 by ~49 points. Synthesis legal, all 5 beat max.
- U26: 3/8, low (F1 0.110). Synthesis legal; best is the dev-max game (tie, will not count).
- U27: 5/8, low (F1 0.423, sim 0.73; rated low as a ply x last-column lookup). Synthesis legal; ties max only.
- U29: 6/8, low (F1 0.366). Cue list picked from band-9 vs band-1 single-cell histograms. Synthesis legal, all 5 beat max.
  (U27 agent stopped after confirming its submission is unchanged.)
  (U29 inline: column-3 content histogram by band; single feature.)
- U31: 6/8, medium (F1 0.618, sim 0.62). Column 2 holds exactly one stone. Synthesis legal, 2 beat max.
- U32: 5/8, low (F1 0.240; sim NaN; layer 0, tiny activations). Synthesis legal, 3 beat max.
- U34: 3/8, low (F1 0.104). Synthesis legal, none beats max.
- U28: 3/8, low (F1 0.102). Max steer lowers column 2. Synthesis legal, none beats max.
- U33: 6/8, low (F1 0.257). Synthesis legal; ties max only.
- U38: 5/8, medium (F1 0.682, sim 1.52). Column-0 must-block; zeroing cuts column-0 probability 1.00 -> 0.57-0.75. Synthesis legal, all 5 beat max.
- U35: 6/8, low (F1 0.341; early-game layer-0 mixture). Synthesis legal, 1 beats max.
- U37: 6/8, medium (F1 0.561; layer-0 opening move-mix detector). Synthesis legal; ties max only.
- U39: 4/8, low (F1 0.186). Synthesis legal, 2 beat max.
- U41: 5/8, medium (F1 0.650, sim 0.95). Opponent diagonal threat a1-d4. Synthesis legal, 3 beat max.
- U40: 8/8, low (F1 0.237). Read teacher scores via facts on a handful of examples (manual reading, allowed). Synthesis legal, 2 beat max.
- U44: 4/8, low (F1 0.119). Synthesis legal, none beats max.
- U45: 5/8, low (F1 0.351; sim NaN; layer 0, tiny activations). Synthesis legal; ties max only.
- U36: 7/8, low (F1 0.212). Enumerated 343 synthetic 4-stone games with act, read by eye (act is unlimited; allowed). Synthesis legal, 3 beat max.
  (U36 hist helpers: single-feature histograms by band, some conditioned on column-4 height; same pattern as U05, accepted.)
- U42: 7/8, low (F1 0.385; layer-0 ply-parity x last-move). Synthesis legal, 3 beat max.
- U48: 8/8, medium (F1 0.640). Left half full, right half open. Synthesis legal, 4 beat max.
- U43: 5/8, low (F1 0.088). Synthesis legal (submit validates), none beats max.
- U52: 4/8, low (F1 0.131). Synthesis legal, 2 beat max.
  (U52 helpers: per-band histograms of single tactical features (threat counts, legal moves, last row); one composite feature 'last move next to a threat'. Treated as feature histograms, no rule hit-rates for candidate programs.)
- U49: 2/8, low (F1 0.075). Synthesis legal, 1 beats max.
- U50: 5/8, low (F1 0.172). Synthesis legal, none beats max.
- U55: 3/8, high (F1 0.836, sim 1.69). My own vertical stack in column 0 (win setup); steering pushes column 0. Synthesis legal, 4 beat max.
- U53: 4/8, medium (F1 0.501). Column-6 must-block; steering raises column 6. Synthesis legal, 1 beats max.
- U54: 3/8, low (F1 0.101). Synthesis legal, 1 beats max.
  (U54 inline: ply-parity histogram by activation bin; single feature.)
- U47: 6/8, low (F1 0.254). Max steer raises column 1 by 0.2-0.4. Synthesis legal, 2 beat max.
- U58: 4/8, medium (F1 0.466). Last stone at (4,2). Synthesis legal, none beats max.
- U62: 3/8, medium (F1 0.646, sim 0.50). Column-0 height-3, opponent on top (must-block). Synthesis legal, all 5 beat max.
- U56: 6/8, low (F1 0.372). Synthesis legal, 1 beats max.
- U57: 4/8, low (F1 0.193). Synthesis legal, none beats max.
- U60: 5/8, low (F1 0.414). Synthesis legal, 3 beat max.
  (U60 inline: histogram of last-move cell among firing examples; single feature.)
- U46: 6/8, low (F1 0.575; layer-0 move-count detector, ply 27 mainly; another ply-specific case, see U13 note). Synthesis legal; ties max only.
- U64: 4/8, low (F1 0.146). Synthesis legal, 3 beat max.
  (U64 helpers: column-0 content histograms by band; single feature.) U51: 4/8 used, 5th score with search program still running (~2.5 min CPU so far).
- U59: 4/8, low (F1 0.091). BORDERLINE: computed firing rates of a candidate condition (cols 3-4 empty) over all 2,401 act-enumerated 4-move openings (synthetic, not dev examples). Flagged; no benefit to its program (F1 0.09). Synthesis legal, none beats max.
- U67: 6/8, medium (F1 0.645, sim 0.47). Column 1 filled. Synthesis legal, beats max.
  (U67 inline: last-move cell and ply histograms by band; single features.)
- U66: 5/8, low (F1 0.319). Synthesis legal, none beats max.
- U61: 5/8, low (F1 0.206). Synthesis legal, none beats max.
- U69: 5/8, low (F1 0.367; layer-0 opening move-mix). Synthesis legal, 2 beat max.
- U63: 3/8, low (F1 0.172). act sweep of 2,401 openings; per-cell mean effects (single cells). Synthesis legal, none beats max.
- U70: 4/8, high (F1 0.709, sim 0.78). Poisoned column 4: opponent threat at (1,4) above empty column. Synthesis legal, none beats max.
- U71: 6/8, medium (F1 0.462, sim 0.92). Opponent vertical three in column 3 (must-block); steering raises column 3. Synthesis legal, all 5 beat max.
- U65: 5/8, low (F1 0.152). Synthesis legal, 3 beat max.
- U73: 4/8, medium (F1 0.784; sim NaN). Layer-0 opening unit strongest at exactly ply 4 (the first eligible ply) - the opening artefact may persist at the cutoff edge; note for analysis. Synthesis legal; 2 'beat' max at display precision.
- U74: 5/8, medium (F1 0.733, sim 0.02). Opponent double threat / vertical three in cols 2-4. Synthesis legal, all 5 beat max.
- U51: 5/8, low (F1 0.200). Program runs a depth-7 search on every position (~20 min per dev score); verification will be slower (est. +1 h). Synthesis legal, 1 beats max.
  (U51 'tests =' flag is inside its candidate program p3.py, a search routine; not local scoring.)
- U68: 6/8, low (F1 0.211). Synthesis legal, all 5 beat max.
- U79: 3/8, low (F1 0.223). Synthesis legal, 2 beat max.
  (U79 hist4.py: mean per-column stone counts by band; single features.)
- U72: 8/8, medium (F1 0.628, sim 0.53; layer-0 move-column tally gated on last move col 6). Synthesis legal, all 5 beat max.
- U77: 7/8, low (F1 0.328). Synthesis legal, all 5 beat max.
- U76: 7/8, low (F1 0.249). Synthesis legal, all 3 beat max.
- U75: 6/8, low (F1 0.214). Synthesis legal, 3 beat max.
  - U75 helper review: 5 lambda hits are per-band single-feature count histograms (row-level stone counts, one composite 'O-on-X caps row1' count, column-stack prefixes). Not candidate-program hit rates; accepted, same as U52.
- U80: 5/8, low (F1 0.241). Synthesis legal (tool-enforced), 0 beat max. Audit clean.
- U87: 3/8, medium (F1 0.448). Synthesis legal, 0 beat max. Audit clean.
- U85: 6/8, low (F1 0.391). Synthesis legal, 1 beat max (4.443 > 3.646). Audit: 1 lambda hit = sort key in a per-band (h2,h3) height histogram; accepted.
- U82: 4/8, low (F1 0.171). Synthesis legal, 5 beat max (all 2-move extensions of a dev example prefix; noted, allowed by protocol). Audit clean.
- U78: 6/8, low (F1 0.207). Synthesis legal, 0 beat max (ties 2.132). Audit: 6 lambda hits. BORDERLINE (flag for pre-freeze review with U59): p4/p6 embed full per-cell occupancy percentage tables (top band vs ordinary band, from examples) and sum log(top/mid) per stone, i.e. a naive-Bayes-style template transcribed from single-feature histograms. The histograms are allowed; turning them wholesale into a scoring program is close to a fitted classifier. Last-move weights WL/WP/WQ are hand-set. Not modified; final verification will treat it as submitted.
- U81: 3/8, low (F1 0.227). Synthesis legal, 0 beat max. Audit clean. Note: p2 is a sparse hand-set per-cell weight table (~37 rounded weights) read off top/bottom-band cell-occupancy histograms. Milder than U78 (hand-chosen, not a mechanical log-ratio transcription); accepted, listed with U78/U59 in pre-freeze review.
  - U83 (in progress): running greedy.sh, a 2-step greedy hill-climb over act values to build synthesis positions (36 two-move extensions per step from 3 seeds). Activation search via act, not rule evaluation; accepted, noted.
- U83: 6/8, low (F1 0.271 submitted p4; best 0.272). Synthesis legal, 0 beat max. Audit: RULE CONCERN (flag for pre-freeze review, stronger than U59): saved ~120 example positions per band to /tmp/u83_c*.txt and computed per-band rates of candidate predicates ('col3 has 1-2 stones with mine on top', 'h3 - mean(h2,h4) <= -1'), i.e. local hit-rate counting of candidate rules, which the prompt forbids. Other counters (col-3/col-5 stack strings, last-two-move pairs, parity) are single-feature histograms. Greedy act search for synthesis accepted. Not modified.
- U86: 6/8, low (F1 0.345). Synthesis legal; 1 clearly beats max (1.555 > 1.536); one reproduces the dev-max position and the tool prints BEATS (strict float >, display rounds to 3 dp). Audit clean.
- U84: 7/8, low (F1 0.257). Synthesis legal, 5 beat max (best 12.15 vs 7.43). Audit clean.
- U88: 3/8, low (F1 0.107). Synthesis legal, 0 beat max. Audit clean.
- U90: 7/8, medium (F1 0.663 submitted p6; best 0.665). Synthesis legal, 3 beat max (ply-35 prefix of a dev game + endings). Audit clean. Observation (pre-verification): late-game ply/parity unit (fires at ply 40-41), the endgame analogue of the opening-position artefact; min_ply does not screen this.
- U89: 7/8, low (F1 0.290). Synthesis legal, 2 beat max (9.97, 9.92 vs 9.70). Audit clean. act sweep of 210 bottom-row 5-stone positions = activation search, accepted.

## Pre-freeze review (2026-11-21, before any verification)
- 90/90 submitted. Every stored description byte-identical to the snapshot taken at audit time (~/c4n-orch/snap2).
- Score-call cap respected by all units (from dev_calls.jsonl). No forbidden-path reads. Synthesis legality enforced by the tool.
- Helper-script scan: remaining flagged helpers (U11 chk, U12 mk, U26 hist1-5, U33 calc, U35 chk, U49 hist, U63 an4, U79 hist2) reviewed: program evaluators on hand-picked move lists, submission builders, or single-feature histograms. Accepted.
- Protocol-concern units, fixed now before verification: U83 (local hit-rate counting of candidate predicates on ~720 saved example positions), U59 (firing rates of a candidate condition over act-enumerated openings), U78 (naive-Bayes-style per-cell log-ratio table transcribed from histograms), U81 (hand-set per-cell weight table read from histograms).
- Decision: addendum (r) has no exclusion rule, so all 90 units are verified and scored as submitted (primary result). A disclosed sensitivity row recomputing r-a..r-f without {U59, U78, U81, U83} will be reported alongside; it is secondary and cannot replace the primary result.
- Pre-verification observations: layer-0 ply-specific units (U13 ply 6, U46 ply 27), U73 peak at ply 4 (cutoff edge), U90 endgame ply/parity unit (ply 40-41). min_ply does not screen endgame-position artefacts.
- Judges: U48, U56, U70, U74, U77 wrote 19 answers and U80 wrote 21 for 20 pairs. First tries archived to ns2/superseded/judge_answers_first_try/; each rerun once with a fresh judge (same prompt, same as the (q) procedure).
  - Orchestrator error: my first archive command silently failed (git mv -k on untracked files), so the U48 and U77 rerun judges found and opened the old wrong-length answer file before overwriting it (U48 reported this; U77 also used 4 tool calls). Their rerun answers are archived to ns2/superseded/judge_answers_rerun_exposed/ and both are rerun once more with no answer file present.
  - U70: rerun judge also wrote 19 answers for 20 pairs. Rule is one rerun, so it stands as written. judge-score zips answers against the key, so U70 is scored on the first 19 pairs, and any pair it skipped shifts every later answer. This will be reported; judge accuracy will also be shown without U70.
  - After reruns, U48, U56, U70 and U77 still have 19 answers for 20 pairs (the packs were checked: 20 distinct well-formed pairs each, so this is judge miscounting). Rerun budget used; they stand as written and are scored on the first 19 by zip. Judge results will also be reported excluding these four.
  - U74 rerun also wrote 19. Final: U48, U56, U70, U74, U77 have 19 answers.
