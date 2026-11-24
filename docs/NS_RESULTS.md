# Neuron Scientist: results of studies (q) and (r)

Pre-registrations: `docs/PLAN.md` addenda (q) and (r). Full per-unit tables: `ns/report.md`, `ns2/report.md`.
Audit trails: `ns/orchestrator_log.md`, `ns2/orchestrator_log.md`. Every number below comes from those files; nothing
was re-run or re-scored after verification.

## Headline

Agent descriptions of real neurons beat a 659-concept dictionary and are readable by a text-only judge for the
"explained" units, but in both studies they are **not reliably better than descriptions of random directions**, and
their `level` programs recover little of what the neurons do (simulation share). Study (r) removed the
opening-position artefact that sank (q), and random directions dropped from F1 0.58 to 0.22, but agent F1 on real
unexplained units dropped with them (0.35 to 0.25), so the real-vs-random gap is still below the pre-registered bar.

## Summary table (held-out validation games)

| | (q) explained | (q) unexplained | (q) random | (r) explained | (r) unexplained | (r) random |
|---|---|---|---|---|---|---|
| n | 20 | 40 | 10 | 20 | 40 | 30 |
| agent F1 (median) | 0.63 | 0.35 | 0.58 | 0.64 | 0.25 | 0.22 |
| dictionary F1 | 0.45 | 0.17 | 0.16 | 0.43 | 0.14 | 0.17 |
| AUROC | 0.88 | 0.68 | 0.76 | 0.88 | 0.64 | 0.61 |
| simulation share of ceiling | nan | nan | 0.02 | 0.53 | 0.08 | 0.02 |
| synthesis beats dev max | 0.45 | 0.72 | 0.20 | 0.80 | 0.65 | 0.73 |
| rated low confidence | 0.00 | 0.65 | 0.50 | 0.05 | 0.93 | 0.87 |
| text-only judge accuracy | | | | 0.91 | 0.71 | 0.74 |

(q) judge: real 0.83, random 0.84.

## Pre-registered predictions

| test | (q) | (r) |
|---|---|---|
| a: unexplained, agent - dictionary F1 >= 0.15 | HOLDS (+0.164, CI 0.10-0.27) | **FAILS** (+0.108, CI 0.085-0.134) |
| b: explained, agent >= dictionary - 0.05 | HOLDS (0.63 vs 0.45) | HOLDS (0.64 vs 0.43) |
| c: real - random F1 >= 0.2 and random low-confidence >= 0.5 | FAILS (-0.14; 0.50) | **FAILS** (+0.125; 0.87) |
| d: real simulation share median >= 0.5 | FAILS (NaN) | **FAILS** (0.14; predicted to fail) |
| e: text-only judge, real mean >= 0.8 | HOLDS (0.83; random 0.84) | **FAILS** (0.776; random 0.738) |
| f (r only): >= half of real units above random p90 F1 | - | **FAILS** (35%; random p90 = 0.46) |

## What went wrong, plainly

1. **Random directions are not noise in this model.** In (r) the best random direction (U74) is a clean
   "opponent threatens to win next move" detector at F1 0.74; U20 and U15 are endgame column-fill detectors at 0.51.
   The random-direction null is therefore strong, and (c)/(f) compare real neurons against a control that
   partly contains real features. This is a post-hoc reading, not a tested claim.
2. **Position-count artefacts survive the min-ply fix.** Ply/parity units appear at the end of the game too
   (U90 at ply 40-41, U46 at ply 27, U13 at ply 6). min_ply 4 only removed the opening ones. Logged before verification.
3. **Most unexplained neurons stay unexplained.** 93% of (r) unexplained units were rated low confidence by their own
   scientist, and their median F1 is 0.25. The agents were honest about this.
4. **Simulation share is low.** Even good detectors (F1 > 0.6) recover a small share of the ablation effect: the
   programs describe *when* a unit fires, not *how much*.

## Protocol deviations (all logged before the numbers were seen, unless stated)

- Four (r) units did local analysis that is close to or over the common-measurement rule: U83 (counted candidate
  predicates on saved positions), U59 (random direction; rates over enumerated openings), U78 (naive-Bayes-style
  cell table), U81 (hand-set cell weights). All 90 were scored as submitted. Excluding the four does not change any
  verdict: a +0.110, b 0.64 vs 0.43, c gap 0.121, d 0.142, f 36.8% (`ns2/sensitivity.txt`).
- Judges: U48, U56, U70, U74, U77 wrote 19 answers for 20 pairs even after one rerun; they are scored on the first 19
  (zip), which can misalign later answers. Excluding them: real 0.787, random 0.734 (still below 0.8).
  An orchestrator error let the U48 and U77 rerun judges see the earlier wrong-length answer file; those reruns were
  archived and re-done with no file present (`ns2/superseded/`).
- (q) deviations are listed in `ns/orchestrator_log.md` (reruns of U02/U03 and ten units after the scorer rule, synthesis
  sequences replaced where they passed a completed four, six judges rerun).

## What is solid enough for an atlas

The **explained** stratum is consistent across both studies: median F1 0.63-0.64 on held-out games, AUROC 0.88,
judge accuracy 0.91 in (r), and simulation share 0.53 in (r). 44 real units across the two studies reach held-out
F1 >= 0.5, most of them in layers 0-2 describing column states (a column exactly k stones high with a given colour on
top, a full edge column), the opponent's last drop, and in later layers threats and won positions (for example
(r) U55 L4/185+ F1 0.85, U12 L5/613+ "side to move has a winning position"). These are the candidates for an atlas
entry, each with its held-out F1, dictionary baseline, judge score and confidence shown next to it. Units below the
bar, and every random-direction control, should be shown as such rather than dropped.
