# Lab notebook

Dated, factual record of what was run, why, and what came out. Newest entries at the bottom.
Numbers here are working notes; numbers in reports come from `results/` files written by scripts.

## 2026-11-18

**Plan.** Wrote `docs/PLAN.md` (questions Q1–Q6, metrics, pre-registered expectations E1–E4) before any training.

**Engine.** `engine/c4.c`: bitboard Connect Four (column-major, 7 bits per column), threat-cell computation
(Pons' `compute_winning_position`), and a depth-limited negamax teacher.
- Design choice: the transposition table only returns a hit when the stored depth equals the requested depth.
  This makes every score the exact depth-d minimax value, independent of search history, move ordering and table
  size, so the teacher is a pure function of (position, depth). Test: `test_gen_game_deterministic` generates a
  game, pollutes the table with an unrelated deeper search, and regenerates the same game bit-for-bit.
- Leaf heuristic (mover's view): 4 × (own threat cells − opponent's) + 2 × (own threats directly above a playable
  cell − opponent's) + 1 × (own centre-column stones − opponent's). Wins score 1000 − ply of the winning stone.
- Verified against brute force (`tests/test_engine.py`): threat cells on 60 random games at every ply; the teacher
  takes an immediate win and blocks an immediate loss; concept labels for must-block and full columns.
- Speed on Apple M4 Pro, one core: 0.04 / 0.16 / 0.72 ms per position at depth 6 / 8 / 10.
- Strength check (argmax play, 40 two-random-ply openings × both colours): depth 10 vs depth 6 won 59, lost 16,
  drew 5 of 80. Depth 10 chosen as the teacher.

**Target temperature.** Mean entropy of the teacher policy over 50 games at depth 10: 0.78 nats (T=1), 1.04 (T=2),
1.23 (T=4). Chose T=2 for sampling the teacher's moves when generating games (diversity) and T=1 for the training
targets (sharper policy to imitate). Both are recorded in `configs/base.yaml`.

**Cross-platform determinism fix.** The first version sampled moves with libm `exp()`, whose last-bit results can
differ between macOS and glibc, which would change sampled games across machines. Replaced with `det_exp()`, a
range-reduced Taylor series using only IEEE + − × ÷ (correctly rounded everywhere), and compile with
`-ffp-contract=off` to forbid fused multiply-adds. `scripts/check_determinism.py N` regenerates the first N
training games and prints their content hash; on the Linux x86-64 GPU host the first 2,000 games hash to
`e9d05db59ce73388cb477020be0efbf48ab02015f2893c8cdf1854150a4452e8`. A second-platform comparison is still to do.

**Smoke test.** 3k games at depth 4, 60 steps on Apple-silicon MPS: validation KL to teacher fell from 1.11 to 0.80, raw top-1
legality from 0.89 to 1.00. Found and fixed an evaluation bug (fixed 5,000-game loop assumed a 5,000-game split,
producing empty batches on a smaller split).

**Compute.** RunPod RTX 4090 (Secure Cloud, EU-RO-1), image `runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404`,
driver 595.112.07, 48 logical CPUs visible. Environment installed from `uv.lock` (torch 2.9.0+cu128). All 4 tests
pass on the host.

**Provenance.** Every output now gets `<file>.meta.json`: command, UTC time, sha256 over all source files, the full
config, library versions, platform and GPU, and the output's hash. For `.npz` files the hash of the array contents
is recorded too, because npz archives embed timestamps.

**Execution policy.** All generation, training and analysis run on the GPU host; the development machine only edits
code and syncs (`scripts/pod.sh push|pull|run`). The full dataset (400k / 5k / 10k games) is generated on the host.

**End-to-end smoke run** (`C4N_CONFIG=smoke`: 3k games, depth-4 teacher, 60 steps) of every stage on the host.
Bugs found and fixed: (1) the random-rotation baseline ran QR on a CPU saturated by the data generator and stalled;
QR now runs on the GPU from seeded CPU Gaussians; (2) a decorator was displaced by an edit, so damage computation
tracked gradients; (3) poles with no firings above threshold crashed mode clustering; they are now recorded as
skipped (`modes.min_firings`); (4) relative checkpoint paths. Observation: in the 60-step model the best-matching
concepts are game phase and single cells, which positional embeddings provide for free; results will therefore be
broken down by concept family.

**Decomposition test.** `tests/test_trace.py` checks that the per-component contributions to a neuron's gate and up
pre-activations sum to the true values (atol 1e-4) on a randomly perturbed 3-layer model.

**Metric fix from the smoke run (before any main-run result).** The threshold sweep for "best concept F1" originally
went down to p50. On the smoke model it gave every pole, and every random direction, F1 >= 0.5 (median 0.655 vs
0.659): at low thresholds a pole fires on half the positions and trivially matches half-frequency concepts such as
empty cells early in the game. The sweep is now restricted to the tail, thresholds p90–p99.5 (a pole fires on at most
10% of positions), which is what "a pole fires" means in the paper. The p97 metric is unchanged and stays primary.

**JS port.** `web/c4model.js` (no dependencies) against PyTorch on float16-rounded weights over 5 analysis games:
max |logit difference| 2.3e-6, max |activation difference| 3.9e-7, greedy move agreement 100%. Full-sequence
forward takes 1.7 s per game on the (busy) host CPU; the demo will use incremental decoding.

## 2026-11-19

**Main dataset** (GPU host, 48 logical CPUs, depth-10 teacher; `runs/01_generate_data.log`):

| split | games | mean length | unique sequences | first / second / draw | time |
|---|---|---|---|---|---|
| train | 400,000 | 34.4 | 396,504 | 183,217 / 180,480 / 36,303 | 2,624 s |
| val | 5,000 | 34.3 | 5,000 | 2,284 / 2,251 / 465 | 22 s |
| analysis | 10,000 | 34.4 | 9,997 | 4,623 / 4,427 / 950 | 89 s |

About 0.9% of training games repeat another training game (random openings plus a sharp teacher can coincide);
they are kept, as they are a property of the teacher's distribution.

**Main training run** (RTX 4090, 8,000 steps × 512 games, 6.31M parameters, 350 s). Validation at step 8,000:
soft cross-entropy 0.907, KL to the teacher's policy 0.159 nats, legal probability mass 0.9998, top-1 legal 100%,
greedy legal move is one of the teacher's best moves at 94.0% of positions.

**Play strength** (`results/play_main_step_008000.json`; 98 games per opponent: every 2-ply opening × both colours;
model greedy, teacher argmax):

| opponent | win | draw | loss |
|---|---|---|---|
| random | 1.00 | 0.00 | 0.00 |
| teacher depth 1 | 0.77 | 0.06 | 0.17 |
| teacher depth 2 | 0.69 | 0.15 | 0.15 |
| teacher depth 4 | 0.80 | 0.10 | 0.10 |
| teacher depth 6 | 0.73 | 0.12 | 0.14 |
| teacher depth 8 | 0.63 | 0.15 | 0.21 |
| teacher depth 10 | 0.51 | 0.18 | 0.31 |

The model wins more than it loses against its own teacher played greedily. A plausible reason, not yet tested: it
imitates the teacher's whole score distribution over many positions, which averages out horizon errors of a single
depth-10 search. The non-monotonic depth 1–4 results come from only 98 deterministic games per row.

**Q1 functional sparsity** (`results/sparsity.json`; 5,000 analysis games, 170k positions; agreement = greedy legal
move is one of the teacher's best; play = win rate over 98 games):

| condition | zeroed | KL | agree | win vs d4 | win vs d10 |
|---|---|---|---|---|---|
| intact | 0% | 0 | 0.940 | 0.80 | 0.51 |
| zero P25–P75 | 49.9% | 0.043 | 0.923 | 0.80 | 0.44 |
| zero P10–P90 | 79.9% | 0.375 | 0.801 | 0.32 | 0.08 |
| zero P5–P95 | 89.9% | 0.833 | 0.656 | 0.12 | 0.01 |
| zero P3–P97 | 93.8% | 1.132 | 0.573 | 0.03 | 0.00 |
| keep top-64 / layer | 93.8% | 0.253 | 0.821 | 0.38 | 0.20 |
| keep random-64 / layer | 93.8% | 1.361 | 0.411 | 0.00 | 0.00 |
| keep top-256 / layer | 75.0% | 0.028 | 0.926 | 0.74 | 0.46 |

Pre-registered E1 (zeroing P5–P95 costs < 5 points of agreement) **does not hold**: it costs 28.4 points. This
6.3M-parameter dense model is much less functionally sparse than the 35B MoE model in Tigges et al. Magnitude still
carries most of the function: keeping the top 64 of 1,024 neurons per layer and position keeps 82% agreement,
against 41% for 64 random neurons; dropping only the top 8 per layer costs 30 points.

**Quadrants.** All activations: (gate+, up+) 17.8%, (gate+, up−) 18.1%, (gate−, up−) 32.1%, (gate−, up+) 32.1%.
Firings beyond p97/p3: 43.4%, 43.4%, 6.6%, 6.6%. The negative-gate quadrants are two thirds of all activations but 13%
of firings, the same pattern the paper reports for its most causal cells.

**Q2/Q3 concept matching** (`results/concepts_summary.json`; 12,288 poles):
- neuron basis: median best-concept F1 at p97 0.154; poles with F1 >= 0.5: 0.7%; best over tail thresholds
  (p90–p99.5): median 0.256, 4.4% >= 0.5, 0.2% >= 0.8;
- random rotation of each layer: median 0.171 at p97; tail-sweep median 0.286, 7.5% >= 0.5.

Pre-registered E2 (>= 30% of poles reach F1 >= 0.5, and neurons beat random directions) **does not hold** on either
count. The best single matches are board-geometry concepts: full column (F1 up to 0.94) and landing height
(up to 0.92). Pole pairs: the two poles of a neuron share their best concept 8.2% of the time (2.3% for random
pairs) and its family 30.2% (18.8%).

Caveat to examine before concluding: a pole may encode a concept outside the labelled vocabulary (for example a
specific three-in-a-row segment or a conjunction), which F1 against single labelled concepts cannot detect. The
random-rotation control is unaffected by this, because both bases are scored against the same vocabulary.

**Q4 modes** (`results/modes.json`; 240 random poles, 40 per layer, none skipped): median 3 modes per pole (mean 3.10),
median 12 subcircuits; 18.3% of poles have a single mode; 45.4% have one mode carrying >= 90% of their KL damage; for
multi-mode poles the median damage outside the main mode is 17.4%. By layer, the >= 90% share is 0.40, 0.42, 0.40,
0.47, 0.45, 0.57 (layers 0–5). The 30 best concept-matched poles: median 1.5 modes, 70% with a >= 90% main mode.
Reference values in Tigges et al.: median 1 mode, mean 2.82, 69% of poles >= 90%, median 14% outside the main mode.
The pre-registered E3 (median pole has one dominant mode) holds for concept-matched poles and not for random ones.

**Q5 action** (`results/action.json`; 53 poles whose best concept is win_now / block_now / poison / teacher_best
with F1 >= 0.5):
- necessity: zeroing one pole changes the rate of playing its column where the concept holds by a median of 0.14
  points (largest drop 8.8 points, L5·N707− "win now in column 3": 85.3% → 79.6%); random same-layer neurons change
  it by the same amount. Single concept poles are redundant;
- sufficiency: clamping a pole to its p99.5 value at the evaluated position shifts play toward the column by a median
  of 4.7 points, by more than 10 points for 22 of 53 poles. Examples: L5·N267− (block column 3) 16.4% → 51.5%;
  L5·N707− (win column 3) 17.9% → 35.5%; L5·N344− (poisoned column 1) lowers play of column 1 from 11.3% to 2.3%.

**Q6 formation** (`results/dynamics.json`; 2,000 analysis games, 17 checkpoints). Block rate passes 85% at step 800
and 89% at step 1,000, when the best pole whose top concept is block_now_any has F1 0.33 and 0.44 (it plateaus near
0.58 from step 1,500). Take-win rate passes 90% at step 2,000, when the best win_now_any pole has F1 0.20 (0.69 at step
8,000). Pre-registered E4 (dedicated poles before reliable behaviour) **does not hold**: behaviour comes first, and
single-neuron alignment keeps sharpening long after the behaviour has saturated. Caveat: "best pole" counts only
poles whose top concept is the tracked one.

**Compute so far.** RTX 4090, Secure Cloud, $0.89/hr, about 1.3 hours (02:20–03:37 UTC), terminated after all outputs
were copied and verified against the host's MANIFEST.sha256 (41 files). Later work moves to a cheaper card.

**Demo.** Verified in a browser: the page loads the 12.6 MB model, plays, and lists firing poles without console
errors. Trivial families (game phase, side to move, last column) are hidden from the list. Because single-pole
ablation is redundant (Q5), the demo needs group switch-off (all poles of a concept) and a "force on" control
before it can show the model acting on a neuron.

**Second iteration plan (2026-11-19).** (1) Concept vocabulary extended with 276 line concepts (69 four-cell lines ×
{open two, open three} × {mine, theirs}); a brute-force test covers them. Concept caches are keyed by a hash of the
vocabulary. (2) `07b_group_action.py`: rank every pole by F1 against one action concept, then zero the top-k neurons
(k = 1–200) against layer-matched random neurons, and clamp the top-k on. (3) Width sweep, pre-registered in
PLAN.md addendum (c). The main model's concept, mode, action and demo outputs are recomputed with the new vocabulary
at the end of the sweep; the earlier versions are in commit 497a0b2.

**Sweep launched** 2026-11-19 05:04 UTC on an RTX A4500 (Secure Cloud, $0.25/hr; no Community A4500 was free),
pod with 12 vCPUs and 62 GB RAM requested (251 GB visible). Before launch on this host: 6/6 tests pass; smoke runs
of 05 (with line concepts), 07b, 09 and the JS port check pass. Bugs caught by the smoke run: a mis-indented block in
02_train left by an earlier bulk edit; `runs/` missing on a fresh host; a config key under the wrong block. Smoke
outputs now go to `build/results_smoke` so they cannot mix with real results. Queued after the sweep: Q7 (SAE vs
neurons, PLAN addendum d), `10_sweep_summary.py` (mechanical test of W1–W3), JS port check, manifest.
w256 seed 1 trains at ~13 steps/s (8,000 steps in ~10 minutes).

**Sweep interruption (2026-11-19 07:38 UTC).** d_ff 2048 seed 1 trained and played normally but its analysis stages failed
with CUDA out-of-memory on the 20 GB card: sorting a whole layer of activations (170k positions x 2,048 neurons) at once
needs more memory than is free. The sweep runner was stopped and the code fixed: percentile and pole-concept scoring now
process 512 neurons at a time (`c4n/analysis.py`, `scripts/07b_group_action.py`). Per-neuron quantities are independent
of one another, so results do not change; `tests/test_analysis.py` checks chunked against unchunked output (identical
percentiles; F1 equal to 1e-6 including the rotation baseline). The runs for d_ff 256-1024 were computed before this change
with the unchunked code, so their `.meta.json` source hashes differ from later runs'; their numbers are what the
chunked code gives. The runner resumed with the d_ff 2048 seed 1 analysis stages (completed stages are skipped).
Cost so far on the A4500: about 2h45m at $0.25/hr.

## 2026-11-19 (second run): width sweep, SAE comparison, group ablation

Sweep: d_ff in {256, 512, 1,024, 2,048, 4,096} (2.8M to 20.5M parameters), two training seeds each, everything else as the
main run (`results/sweep_summary.json`, per-run files in `results/sweep/`). Seed-mean values; the two seeds agree closely
where trends are claimed (values per seed in the summary file).

| d_ff | agree w/ teacher | score vs depth-10 | cost of zeroing P5-P95 (agree pts) | poles F1>=0.5, neurons | same, random rotation | one mode >= 90% damage | firings in gate+ quadrants |
|---|---|---|---|---|---|---|---|
| 256 | 0.928 | 0.55 | 0.288 | 12.0% | 10.1% | 74% | 94% |
| 512 | 0.934 | 0.58 | 0.247 | 7.6% | 9.0% | 66% | 90% |
| 1,024 | 0.940 | 0.55 | 0.276 | 5.2% | 8.6% | 63% | 87% |
| 2,048 | 0.942 | 0.54 | 0.345 | 3.6% | 7.3% | 55% | 82% |
| 4,096 | 0.944 | 0.57 | 0.395 | 2.6% | 7.2% | 52% | 77% |

(score vs depth-10 = wins + half draws over 98 games, so +-0.05 noise; F1 is the tail-threshold sweep, p90-p99.5.)

**Pre-registered width predictions (PLAN addendum c), scored by `scripts/10_sweep_summary.py`: all three fail, in the
opposite direction.**
- W1 (sparsity cost falls with width): it rises, 0.288 to 0.395, non-monotone at the start (Spearman +0.7 with log width).
- W2 (neuron advantage over random rotations grows, positive at 4,096): the difference falls from +1.8 points to -4.6
  points (Spearman -1.0); neurons beat random directions only at the narrowest width.
- W3 (single-mode share rises): it falls from 74% to 52% (Spearman -1.0).
Skill is about flat across widths (agreement 0.928 to 0.944, score vs depth-10 within noise), so these trends are not a
skill effect. Reading: in this setting a wider MLP spreads each function over more neurons, making the neuron basis less,
not more, privileged. This is the opposite of the trend one would extrapolate toward Goodfire's much wider model, and we
cannot say what happens at their scale, other differences (MoE routing, language data, depth) remain.

**By concept family, main model (d_ff 1,024, 659 concepts incl. lines).** The aggregate hides a split. Poles whose best
concept reaches F1 >= 0.5, neurons vs random rotations: open lines 159 vs 47, landing cell 125 vs 0, board cells 78 vs 14,
last-move column 49 vs 0 (neurons win on local, sparse concepts); but "column is full" 85 vs 712 and game phase 97 vs 172
(random directions win on dense, global ones: a global feature is spread over many neurons, so a random mix captures it
better than any one neuron). Aggregate share: neurons 5.4%, rotations 7.8%.

**Q5b group ablation, main model (`results/group_action.json`; top-k poles ranked by F1 for the concept).**

| concept | k | rate where concept holds: intact / k neurons off / k random neurons off | rate where it does not: intact / k forced on |
|---|---|---|---|
| must block col c | 1 | 0.913 / 0.910 / 0.913 | 0.164 / 0.407 |
| must block col c | 5 | 0.913 / 0.853 / 0.914 | 0.164 / 0.873 |
| must block col c | 20 | 0.913 / 0.724 / 0.913 | 0.164 / 0.946 |
| must block col c | 50 | 0.913 / 0.666 / 0.911 | 0.164 / 0.975 |
| win now col c | 20 | 0.836 / 0.749 / 0.837 | 0.173 / 0.394 |
| win now col c | 50 | 0.836 / 0.715 / 0.837 | 0.173 / 0.516 |

(mean over the 7 columns; 3 random draws per cell.) W4 holds: from k = 5, switching off the concept-ranked neurons lowers the
behaviour while the same number of random same-layer neurons changes nothing; the function is causal but spread over
tens of neurons, not one. Forcing the top 20 "must block" neurons on makes the model play that column 95% of the time
where it is not needed. Win-taking is more distributed and less steerable than blocking.

**Q7 neurons vs a TopK SAE (`results/sae.json`; 4,096 latents per layer, k = 32; FVU 0.006 to 0.19 across layers).**
56% of latents (13,761 of 24,576) fire on < 0.5% of positions and are excluded as dead or rare, so the SAE is under-trained
and this comparison is weak. Over the 10,815 live latents: share with F1 >= 0.5 is 2.3% at p97 and 3.7% best-over-tail
thresholds; for neuron poles 1.0% at p97 and 5.4% best-over-tail (9.7% taking the better pole of each neuron). Prediction
S1 holds at the primary p97 criterion and fails at the threshold sweep: inconclusive. A properly tuned SAE (dead-latent
resampling, longer training, a k and width sweep) is needed before any claim.

**Process.** Cost: A4500 from 04:55 to about 11:33 UTC at $0.25/hr, about $1.65, terminated after the 192 pulled files matched
the host manifest; with the 4090 run earlier, about $2.80 of RunPod credit spent in total. One interruption (GPU
out-of-memory at d_ff 2,048, fixed by chunking, see above).

## 2026-11-20: blog post built

`docs/blog/` holds the post: `post.tpl.html` (template), `scripts/12_build_blog.py` (fills it from `results/`; fails on a
missing value, and asserts every direction claim in the prose, for example which basis wins on which concept family, that
W1-W3 failed in all seeds, that the "behaviour before neurons" claim holds), `assets/c4charts.js` (four figures),
`demo/` (the in-browser model, copied from `web/`), generated `index.html` and `data/figures.js`. Checked in the browser:
no console errors; all four figures, tooltips and the demo work; at a 390 px layout no chart text is clipped and no table
overflows (wide tables scroll). Main text is about 2,000 words including tables and captions.

Correction to an earlier entry: the "Q6 formation" note above says take-win rate passes 90% at step 2,000. It was 89.6% at
step 2,000 and 95.1% at step 3,000; the first checkpoint at or above 90% is step 3,000, where the best "win now" neuron has
F1 0.43. The post uses the computed value. The blocking numbers (85% at step 800, best neuron F1 0.33) are unchanged.

Not done: publishing to the personal site (needs the author's go-ahead), the repository link and weights release
placeholders in the post, an exact-solver optimality measurement.

## 2026-11-21: validity round

Motivation and tests are pre-registered in PLAN.md addendum (e) (committed before any of them ran, dcc98d8). Code:
`13_basis_controls.py` (T1 kurtosis / T2 sparsity vs rotated bases), `14_crossfit.py` (T3 cross-fitted matching with game-level
bootstrap), `make_robust.py` (T5-T7 configs: 32k steps, weight decay 0 / 1.0, d_model 512), extra sweep seeds in
`make_sweep.py` (T4), `run_queue.sh` (resumable runner), `15_validity_summary.py` (decision rules). Blog: the demo now sits
directly under the header and starts by itself on windows at least 720 px wide.

Compute: The A4500 has no stock; no Community RTX 4090 either; Secure
RTX 4090 is $0.89/hr. The main run showed a 4090 trains about 2.9x faster than the A4500 ($0.25/hr), so per unit of work the
cost is similar and wall-clock time is much shorter. Estimated total about 3 GPU-hours (about $2.70), split over two pods.

### Validity tests T1 to T3 (11 models: the main model and the 10 sweep models)

Scored by `scripts/15_validity_summary.py` against the rules in PLAN addendum (e).
- **T1, shape. Held in all 11 models.** Mean excess kurtosis of a unit's activation distribution: 30.5 to 32.0 for neurons against
  4.3 to 6.9 for random rotations of the same layer; share of squared activation in the largest 5% of entries: 85 to 93% against
  48 to 64%. The neuron basis is heavy-tailed in a way no random basis is.
- **T2, function. Held in all 11 models.** Agreement lost by zeroing each unit's central 90%: neurons 24 to 40 points, rotated
  bases 39 to 43 points. The model is not sparse in absolute terms but is sparser in its neurons than in any rotated basis.
  The gap closes with width: neurons lose 24 to 30 points at 256 to 512 neurons per layer and 39 to 40 at 4,096, against a
  constant 41 for rotations. Keeping only the largest 6.25% of units in the main model: neurons 82% agreement, rotations 50 to 53%.
  The earlier statement "not functionally sparse" is therefore qualified: not sparse, but clearly privileged.
- **T3, matching without selection bias. Aggregate part held, local-concept clause did not (in 1 of 7 runs).** Poles choose their
  concept on half of the games and are scored on the other half. Held-out share of poles with F1 >= 0.5, neurons minus random
  rotations: -2.4 points (main), -3.3 and -3.4 (1,024), -3.7 and -3.6 (2,048), -5.3 and -3.9 (4,096), all with 95% intervals that
  exclude zero; at 512 it is -0.9 and -2.2; at 256 it is +2.9 (excludes zero) and +0.5 (includes zero). In-sample and held-out
  shares agree (main: 5.4% and 5.4%), so selection bias was small. By family, neurons win on landing cells, board cells, threat
  cells, win-now and last-move column in all 11 models, and on open lines in 10 (not at 2,048 seed 1: 220 against 246);
  random directions win on "column is full" and game phase in all 11.
- **Net for the width claim.** The "wider is worse for neurons" trend survives the selection-bias correction. T4 to T7 are
  still running at the time of writing.

### Tactic localisation (main model; PLAN addendum f)

`c4n/tactics.py` defines four tactics as labelled decision problems (verified against brute force; the first version of the poison
definition wrongly counted winning moves as poison, which the test caught). Accuracy of the greedy move (chance in brackets):
take the win 98.4% (51%), block 97.0% (23%), avoid a poisoned column 100% (74%), make a fork 75.3% (24%); control (teacher's best
move on random positions) 94.9%. Fork positions are rare (615 in 5,000 games), so that rate has a standard error near 1.7 points.
- **Components.** Mean-ablating layer 0's MLP costs every tactic 25 to 54 points but the control 47 points, and layer 5's MLP
  costs 7 to 44 against 39 for the control: general damage, not tactic-specific. Beyond the control: **block depends on layer 0
  head 3** (55 points lost, control 33; also L0 H2, L0 MLP), **win on layer 0 head 5** (24 against 11), **fork on layer 5**
  (MLP +6, heads 3 and 4 +3 each). Poison avoidance has no component whose removal hurts it beyond the control.
- **Neurons.** Top-50 attribution neurons (tactic accuracy / control accuracy when zeroed; same count of random neurons in
  brackets for the tactic): fork 64% / 94% (76%), block 86% / 93% (97%), win 96% / 93% (98%), poison 99% / 93% (100%). At 200: fork
  48% / 91%, block 64% / 85%, win 88% / 89%, poison 93% / 85%. Fork and block neurons are tactic-specific; win neurons are not
  at this size. Where the top-50 sit: layer 5 holds 42 of block's, 35 of poison's, 21 of win's and 22 of fork's.
- **Training.** Poison avoidance is near ceiling by step 100 (93%), block reaches 82% at step 600 and 97% at 3,000, win 75% at step
  600 and 94% at 3,000, and fork rises slowly to 75%. The components that matter, L0 H3 and the layer 5 MLP, only become
  necessary around steps 1,500 to 4,000 (L0 H3's cost for blocking is 6 points at step 600, 34 at 1,500, 55 at 4,000), long
  after the behaviour first appears: the model first solves the tactics another way and later routes them through these parts.
- **Pre-registered predictions.** P-a (layers 3 to 5 MLP or layers 1 to 4 attention carry most of the drop): **did not hold**;
  the tactic-specific parts are layer 0 attention and layer 5. P-b (top-50 neurons beat 50 random): **held** for all four (poison
  by under 1 point), and tactic-specific for fork and block only. P-c (information decodable before it is used): **not supported**:
  probe AUROC rises smoothly through the layers (win 0.87 at the embeddings to 0.99 after layer 5, block 0.66 to 0.98) with no
  clear lead over the layers that matter. P-d (at most 6 heads carry half the head effect): **held** raw (top 6 carry 74 to 93%);
  after the control only L0 H3, L0 H5 and L5 H3/H4 stand out. "Fork is learned last" held; "depends on more layers" did not.

### Neuron atlas

`scripts/18_atlas_export.py` and `19_build_atlas.py` build `docs/blog/atlas/`: all 6,144 neurons, both poles, each with its
matching concepts (F1), what the board looks like when it fires (difference from baseline for the mover's stones, the
opponent's and empty cells), top activating positions with the move played, direct effect on each column's score (sign flipped
for negative poles), quantiles, and attribution for each tactic; a map of all neurons coloured by concept family or tactic
support; and the component and training-time tables above. 61,440 example positions are checked against the move records at
build time. Example: L5 N344 matches "the opponent threatens to win in column 1" at its positive pole and "playing column 1
hands the opponent a win on top" at its negative pole, and promotes column 1 when the first fires and suppresses it when the second does.

### Demo: switch off parts, load positions where they matter (2026-11-21)

`scripts/20_export_demo_parts.py` exports eight parts (layer 0 heads 3 and 5, layer 5 heads 3 and 4, layer 5 MLP, and the 50 top
neurons for each tactic) with the mean activations that mean-ablation needs, and 10 real positions where switching a part off
flips a tactic the intact model gets right (for example layer 0 head 3 takes a correct block from 100% to 0.5%). The JavaScript
model gained head and MLP mean-ablation; `tests/check_web_port.js` checks it against PyTorch under all 8 ablations (largest logit
difference 1.1e-4, with the shipped float16 weights on both sides). A first reference check failed at 0.026 because it used
float32 weights; that was a reference bug, not a port bug. Note the effect is position-dependent: on the easy bottom-row threat
the model still blocks without layer 0 head 3 (92%), and only the layer 5 MLP breaks it (2%).

### Validity tests T4 to T7, and the full scorecard (2026-11-21, 20 models)

`results/validity_summary.json`. "Gap" = share of poles matching a concept (F1 >= 0.5), neurons minus random rotations, in
points; cross-fitted values (held-out halves, 95% game-bootstrap intervals) agree with in-sample values to within 0.4 points.
- **T4, more seeds. Held.** 256 neurons per layer, 4 seeds: +3.2, +0.5, +1.0, +0.5 (cross-fit intervals exclude zero for seed 1
  only). 1,024, 4 seeds: -3.4, -3.4, -2.5, -3.3 (all exclude zero). 4,096, 2 seeds: -5.3, -3.9. Every paired seed has
  gap(256) > gap(4,096). Neurons are about as good as random directions at 256 and clearly worse from 1,024 up.
- **T5, 4x training. Failed by its letter, direction confirms the claim.** Gap -3.4 -> -4.2 (change -0.8, inside the 2-point bar),
  one-dominant-mode share 65% -> 59% (change -5.4, just outside the 5-point bar). Longer training does not make neurons cleaner; if
  anything slightly less. The result is not an under-training artefact.
- **T6, weight decay. Held (no dependence above 3 points).** Gap -2.9 (wd 0), -3.4 (0.1), -4.5 (1.0). Strong weight decay also
  lowers kurtosis (18 vs 31) and the one-dominant-mode share (38% vs 65%).
- **T7, ratio vs absolute width. Failed.** Gap at d_model 512: -2.5 with 1,024 neurons (ratio 2), -0.7 with 2,048 (ratio 4); at
  d_model 256 with 1,024 (ratio 4): -3.4. The ratio alone does not explain the trend: a wider residual stream makes the neuron
  basis better on every measure (kurtosis 65 to 80 against 30 to 32; one-dominant-mode share 72 to 74% against 52 to 76%; sparsity
  cost 0.21 to 0.27), while a wider MLP at fixed residual width makes it worse.
- **T1, T2 across all 20 models. Held.** Neuron kurtosis 18 to 80 against 3 to 7.5 for rotations; zeroing each unit's central 90%
  costs 21 to 40 points in the neuron basis and 38 to 44 in rotated bases.

**Conclusion supported by everything above.** In this model family the neuron basis is always privileged in shape (heavy tails)
and in function (sparser than any rotation), and individual neurons do carry local concepts (board cells, landing cells, threat
cells, last-move column) better than random directions. Whether neurons beat random directions *overall* at matching concepts
depends on the architecture: roughly even when the MLP is narrow (256 neurons per layer) or the residual stream is wide
(d_model 512, 2,048 neurons), and worse as the MLP widens at a fixed residual width. It does not depend on training length or
weight decay. Global concepts ("column full", game phase) are always better captured by directions than by single neurons.

Compute this round: two Secure RTX 4090 pods ($0.89/hr each). Pod A finished at 07:00 and sat idle until 08:07 because the
completion watcher waited for both pods (about $0.90 wasted; a per-pod watcher would have avoided it). Both terminated after
pulling results.

## 2026-11-21 — Does the model keep a board in its head? (PLAN addenda h, i)

Pod: 1x RTX 4090 Secure ($0.89/h, community 4090/3090 out of stock), ~75 min, terminated. Scripts `21_world_model.py`,
`21b_edit_followup.py`; results `results/world_model*.json`, `world_model.npz`; demo export `web/worldmodel.{json,bin}`
(JS port reproduces the PyTorch edits to 1e-5, `tests/check_web_port.js`).

**W1 board probes (held-out games).** Colour accuracy on occupied cells, relative (mine/theirs) vs absolute (first/second
player): embeddings 35.9 / 35.2, after L0 67.6 / 56.3, L1 79.4 / 56.9, L2 attn 97.7 / 60.9, **L3 attn 98.6** / 61.8, L5 88.5 / 55.9.
The board is built in layers 1-2, peaks after layer 3's attention and fades towards the output. MLP probe adds little (L2 97.9).
Untrained model: colour <= 50% at every point, but emptiness ~97% — emptiness is readable from token/position statistics
alone, so only colour is evidence of a learned board. Per-cell majority-by-move-number baseline: colour 34%.
(W-a) held, (W-b) held.
**W2 threat cells**: AUROC 0.96-0.99 from layer 0 on (mover), peaks L2-L3.
**W3 edits** (W-c, W-d): failed. Held-out colour flips: follow 15.6% (start L0, chosen on the selection half), random
direction of the same norm 10.9%, no edit 0%; preservation 94% (held). Follow rate falls with later start layers (L5: 0%).
**W4 who builds the board**: mean-ablating L0 H3 drops colour accuracy 27 points, L0 H5 15, everything else < 4; L0 MLP 36,
L1 MLP 15. Attention shares: L0 H3 87% on the mover's own past moves; L0 H2 79% on the opponent's; L1 H6 92% own, L1 H4 84%
opponent, L1 H0 79% own. (W-e) held (top 3: L0 H3, H5, H1). L0 H3 and H5 are the heads the tactic atlas found for block and win.
**W5**: failed. Top-50 block neurons' output weights are no more aligned with opponent-threat directions than random
neurons (median max-|cos| 0.104 vs 0.121, p = 1.0); win neurons 0.117 vs 0.110, p = 0.17.
**W6 emergence**: colour readout after L2 rises gradually, 57% at step 400, 79% at 1,000, 95% at 3,000, alongside block (78% to 97%) and win (74% to 94%) over the same steps; poison is near its final rate by step 100, before any board is readable.

**Follow-up (i), exploratory, pre-registered before running.** Strength x4/x8 and edits at every read point from L1 attention:
best board edit 28.9% vs 20.4% random (i-a failed). Editing threat-cell directions: 16.3% vs 13.8% (i-b failed).
**Conclusion.** The model computes a linearly readable board in its own perspective (mine / theirs, not colours), built by a few
early heads that sort past moves by player — the same heads the tactics depend on. But rewriting that board at the current
position barely moves the decision. Decodable is not the same as used: either the move reads the board through other positions
(later layers attend to earlier positions, which still hold the true board) or from a nonlinear / distributed code our linear
probes do not capture. Next test (not run): edit the representation at every position, or patch whole residuals between real
positions that differ in one stone.

## 2026-11-21 — Is the board used? Edits at every position (PLAN addendum j)

Pod: 1x RTX 4090 Secure ($0.89/h), ~35 min, terminated. `scripts/21c_edit_history.py` -> `results/world_model_history.json`
(36 configurations: scope x direction x start x strength, each with a same-norm random control). 22,214 colour flips, 4,543
where the clean model played a teacher-best move that the flip makes wrong.

**(j-a) failed by letter, but is not a null.** Best configuration chosen on the selection half (all positions, probe direction,
p0 = 3 (from layer 1 attention on), k = 2): report half follow rate **41.8%** against **20.2%** for a same-norm random direction
(+21.5 points; bars were 50% and +30), preservation 80%. **(j-b) failed**: at that configuration history-only edits follow
25.9% (random 8.4%, +17.5), current-only 28.3% (random 19.5%, +8.8), all positions 41.8% (random 20.2%, +21.5). By raw follow
rate history is not higher than current; relative to its own random control it is (+17.5 vs +8.8).
Across all 36 runs: editing all positions beats either part alone; mean-difference directions are no better than probe
directions at the best settings (all-positions, p0 = 3, k = 1: 41.0% vs 40.7%); stronger edits (k = 4) always do worse
(preservation 53-66%, random control rises to 22%), so the edit starts breaking the model before it steers it. Random
controls are high (14-22%) because a perturbation that changes the move at all lands on a teacher-best move of the edited
board a fifth of the time; the honest effect size is the gap, not the rate.
**Conclusion, replacing the earlier one.** The board the probes read is partly used: rewriting it at every position where the
stone is visible moves the model to the right move for the edited board about twice as often as random (41.8% vs 20.2%),
and edits to history alone do too. It is not the clean, near-complete steering reported for Othello-GPT, so either the
move depends on this linear board only partly (other, non-board features also feed it: for example direct move-pattern
features, threat features, or a nonlinear board code), or our edit is still too blunt. Not tested: edits through the
attention values only, patching across real positions that differ by one stone, nonlinear probes as the edit direction.

## 2026-11-21 — Treatment vs control board test and the size ladder (PLAN addenda k, l)

Pod: 1x RTX 4090 Secure ($0.89/h), ~55 min, terminated. Scripts `22_board_causal.py`, `run_small.sh`,
`run_ladder.sh`, `23_ladder_summary.py`, `make_small.py`; results `results/board_causal.json` (6-layer),
`results/small/s*/board_causal.json`, `results/ladder/*/board_causal.json`, `results/ladder_summary.json`.
**Test.** Per position (held-out games, clean model plays a teacher-best move): flip one stone that changes the teacher's best
set (treatment) and one that does not (control), same intervention at every position from the one after the stone was played,
at every read point from p0 on. Specificity = P(move changes | relevant) - P(move changes | irrelevant), paired by position,
game-bootstrap interval, configuration chosen on the selection half and scored on the report half.
**6-layer model (k-b): holds.** 1,069 pairs: change 58.0% vs 17.6%, specificity +0.404 [0.368, 0.441], correct new move 75%,
guard (irrelevant: still a best move) 91%. The same-norm random direction changes the move 60% of the time but lands on a
best move of the edited board 19% of the time, which is why the earlier random-direction control was uninformative about change.
**Ladder, 5 seeds each (agree = teacher-best agreement; colour = board colour accuracy at the best read point):**
| size | params | agree | colour | specificity | k-a pass |
|---|---|---|---|---|---|
| 1x64 | 69k | 73.7 | 65.7 | 0.037 | 0/5 |
| 1x128 | 270k | 75.4 | 67.0 | 0.035 | 0/5 |
| 2x64 | 135k | 76.8 | 69.3 | 0.033 | 0/5 |
| 2x128 | 532k | 80.6 | 73.7 | 0.064 | 0/5 |
| 3x64 | 201k | 80.0 | 75.4 | 0.124 | 0/5 |
| 3x128 | 795k | 87.1 | 91.2 | 0.207 (0.157-0.232) | 0/5 |
| 6x256 | 6.3M | 94.0 | 98.6 | 0.404 | 1/1 |
(l-a) held (1-layer agreement 13 points below 3x128). (l-b) held (1-layer colour 66-67%). (l-c) failed: the only sizes with a
readable board (3x128) pass k-a in 0/5 seeds (specificity 0.16-0.23, interval above 0 in all five, correct direction 0.44-0.55).
(k-a) failed in 0/5 small seeds; (k-c) failed (small models are less specific, not more).
**Across all 31 models**, board colour accuracy vs specificity: Pearson 0.93, Spearman 0.88 (agreement vs specificity 0.92);
within the 3x128 family 0.81. Specificity rises smoothly with board quality; there is no sharp threshold in this ladder.
At fixed width depth helps (2x64 -> 3x64: colour 69 -> 75, specificity 0.03 -> 0.12), width helps at fixed depth
(3x64 -> 3x128: 75 -> 91, 0.12 -> 0.21), and 2x128 (532k) is below 3x64 (201k) on both.
**Conclusion.** The move uses the board the probes read, specifically, in the model that holds the best board (6x256). In models
that hold a worse board the effect is smaller but still positive (3x128 all five intervals above 0), and in models with no board
(1-2 layers) it is about zero. Smaller models are not easier here: the board gets worse as the model shrinks, so a clean
treatment-versus-control result needs a model between 795k and 6.3M parameters (untested). Candidate next sizes: 4x192, 4x256,
6x128; or train small models with an auxiliary board loss and compare with and without it.

## 2026-11-21 — Mid-size models: where the board test becomes clean (PLAN addenda m, n)

Pods: the first (EUR-IS-1) booted with `torch.cuda.is_available() == False` and trained on CPU for ~45 min before I noticed
(about $0.65 wasted, plus a ~20 min `uv sync`); replaced. The second pod's upload and install took ~50 min of billing. CUDA guard added to
`run_*.sh`. Final pod terminated; all pods terminated. `results/ladder_summary.json` regenerated (43 models).
| size | params | agree | colour | specificity | direction | k-a pass |
|---|---|---|---|---|---|---|
| 3x128 | 795k | 87.1 | 91.2 | 0.207 | 0.50 | 0/5 |
| 6x128 | 1.58M | 90.4 | 94.4 | 0.261 (0.246-0.284) | 0.66 | 4/5 |
| 4x192 | 2.37M | 91.2 | 95.3 | 0.297 (0.282-0.315) | 0.67 | 5/5 |
| 6x256, 8,000 steps (main) | 6.3M | 94.0 | 98.6 | 0.404 | 0.75 | 1/1 |
| 6x256, 6,000 steps, seeds 2-3 | 6.3M | 93.3 | 98.0 | 0.344 (0.341, 0.347) | 0.72 | 2/2 |
(m-b) holds: 6x128 passes in 4 of 5 seeds (the miss is 0.246, by 0.004) and 4x192 in 5 of 5; the smallest model that passes is 6x128 (1.58M
parameters, 4x192 is the one that passes in every seed). (m-c) holds. (m-a) holds on the four sizes that ran (specificity .207 < .261 <
.297 < .404; colour .912 < .944 < .953 < .986), but is not monotone in raw parameters over the whole ladder (2x128 at 532k is below
3x64 at 201k on both). Across all 43 models, board colour accuracy vs specificity: Pearson 0.97, Spearman 0.95.
The 6x256 models trained for 6,000 steps (0.34) score below the main model's 8,000 steps (0.40), so length matters at the top end.

## 2026-11-21 — Concept mapping in the small models (PLAN addenda o, p)

Pod 19twy8qsqxflda (1x RTX 4090 Secure), ~45 min, terminated. `scripts/24_concept_coverage.py` (new), `14_crossfit.py`, `22_board_causal.py`
on the main model and on retrained 4x192 and 6x128 (seed 1; the earlier ladder checkpoints were not kept; the retrained models are
new training runs and score slightly differently, e.g. board specificity 0.310 / 0.246 vs 0.310 / 0.246 recorded earlier). Queue stopped
after seed 1 at the author's request (addendum p). Results: `results/concept_coverage.json` (main), `results/concept/*/`.
| model | params | agree | board colour | board spec | neuron coverage | random | probe | cross-fit pole gap |
|---|---|---|---|---|---|---|---|---|
| 6x256 (main) | 6.3M | 94.0 | 98.6 | 0.404 | 30.8% | 6.1% | 55.9% | -2.4 [-2.5, -2.2] |
| 4x192 s1 | 2.4M | 91.2 | 95.5 | 0.310 | 21.5% | 6.2% | 53.3% | -5.8 [-5.9, -5.6] |
| 6x128 s1 | 1.6M | 90.5 | 96.0 | 0.246 | 18.2% | 4.9% | 51.9% | -1.3 [-1.5, -1.1] |
Coverage = share of 659 concepts with a unit/direction whose held-out F1 >= 0.5 (selected on the other half of the games).
By family (neuron / random / probe): board cells (210) 25/9/100 (main), 19/11/100 (4x192), 16/6/100 (6x128); landing cell (42)
98/7/100, 85/2/100, 56/2/100; must-block (9) 89/22/89, 61/11/44, 39/11/39; poison (7) 57/0/71, 0/0/57, 0/0/57; open lines (255)
22/3/16, 10/2/13, 11/4/9. Predictions: (o-a) holds on the 3 models tested (gap <= 0, none above +1) but not at the registered 4-of-5
power; (o-b) holds (probe - neuron = 25, 32, 34 points); (o-c) probe coverage of board cells = 100% in both small models, neuron
coverage 19% / 16%; (o-d) FAILED: neuron coverage is lower in the small models (21.5%, 18.2%) than in 6x256 (30.8%).
**Reading.** A linear probe maps the board and most concepts about as completely in the 2.4M and 1.6M models (52-53%) as in the 6.3M
one (56%); single-neuron maps lose about a third of their coverage when the model shrinks, because there are half as many units
and the narrower residual stream splits concepts across them (consistent with T7: smaller d_model hurts the neuron basis). The
exception is the neurons' strongest case, "which column does the last move occupy" (100% everywhere). Seed spread unknown (one seed per size).

## 2026-11-22 — Neuron Scientist studies (q) and (r) received; atlas draft

The separate session ran (q) as registered, then pre-registered and ran follow-up (r) (addendum r: positions with < 4 stones
ineligible, 30 random directions, fresh units). Results, logs and code changes committed unchanged (42ac335); answer keys were not
included and were not opened. Independent recomputation from ns/report.json and ns2/report.json matches docs/NS_RESULTS.md
(medians per stratum, prediction verdicts, 25 + 19 = 44 real units at held-out F1 >= 0.5, five judge files with 19 of 20 answers).
One display difference: their table prints the (q) explained-stratum simulation share as nan; skipping undefined values it is 0.70.
**Post-hoc label (not pre-registered), `scripts/34_ns_opening_label.py`.** Each unit with held-out F1 >= 0.5 is an "opening unit"
if >= 50% of the positions where its frozen program predicts firing (first 1,000 validation games) have fewer than 4 stones.
10 of 53: q-U05, U50, U51, U59, U63 (real) and q-U02, U36, U41, U48, U64 (random); none in (r). So 39 of the 44 well-described real
neurons are not opening artefacts, and 4 of the 9 well-described random directions are not either (best: r-U74, F1 0.74,
"opponent threatens to win next move"). No score was changed.
**Atlas draft** `docs/blog/ns-atlas/` (data from `scripts/33_ns_atlas_export.py`, which asserts the 25/19 counts): cards for all
160 units with description, held-out F1/AUROC, dictionary baseline, judge, simulation, synthesis, confidence, measured steering,
the rule and lab notes; example boards are the atlas's top dev firings for real neurons and the agent's own built positions for
random directions; opening units carry a badge and sort last. Checked at 1280 px and 390 px (no overflow). Not published.

## 2026-11-23 — Blocking circuit (PLAN addendum s, S0-S5): results and freeze

Pod c4-circuit (Secure RTX 4090, $0.89/h, CUDA checked). Tests: tests/test_circuit.py 5/5 (pairs checked against brute force; activations
identical before the last position; patching identities). Full run 150 s. **S5 freeze: results/block_circuit.json sha256 ab817a02aad05381…, committed
before any Test A / Test B computation.**
- Pairs: 19,720 / 19,773 must-block positions (analysis / val); 72% have a valid one-move corruption; 4,000 used per split. Clean block
  accuracy 98.6% / 98.1%; the corrupted twin plays that column 20%. Gap 12.6 nats (val 12.6).
- Circuit rule: the cap was reached below 80% → pre-registered reading **"no compact neuron circuit" for blocking as a whole**; C = top 200
  (layers 0:26, 1:10, 2:7, 3:14, 4:34, 5:109). Joint noising curve: 1 neuron 4%, 10: 22%, 50: 51%, 100: 65%, 200: 77%. Attribution vs exact
  rank correlation 0.87. Top neuron L5 N344+ (4.3%), the neuron the atlas labelled "opponent threatens column 1".
- (s-1) FAILED narrowly: 76.7% [76.0, 77.4] (bar 80%). (s-2) held: random layer-matched sets 0.8% median, 4.2% p95. (s-3) held: denoising
  restores 87.7% [86.8, 88.7]. (s-4) FAILED: mean-ablating C drops block accuracy 96.9% → 64.7% (−32 pts, passes) but control accuracy
  94.8% → 70.7% (−24 pts, bar 5); random sets −0.2 pts. (s-5) FAILED: top heads by last-position noising are L0 H2 (29%), H1, H0; L0 H3 is
  not in the top 3; top MLP is layer 0 (94%), with layer 5 at 93%. (s-6) held: C removes 87% (vertical), 71% (horizontal), 60% (diagonal);
  the same rule within orientation gives a **compact 53-neuron circuit for vertical threats** (52 of them in C) and none (cap) for
  horizontal or diagonal.
- Post-hoc note (not a test): last-position patching measures what carries the *difference* the last move makes; L0 H3 reads the mover's
  own earlier stones, which are identical in both runs, so it can be necessary (atlas, mean-ablation) without carrying the difference.
- Mechanism (descriptive): 65.5% of C's neurons promote (direct logit) the column whose threats they matter most for; held-out probe
  accuracy at the neurons' input points 86% (after L0 attention) to 99%.

### Test A (S6, follow-up on frozen (q)/(r) programs; nothing re-scored) and Test B preparation (S7)

- `results/ns_block_testA.json` (validation, first 2,000 games, >= 4 stones). **12 of the 120 described real neurons are circuit neurons**
  (11 with the same pole; about 2 expected if the (q)/(r) samples were random draws, but the explained stratum favoured dictionary-matched
  neurons). Ranks in C: 5, 6, 9, 12, 13, 22, 47, 96, 98, 109, 130, 188. **8 of the 11 pole-matched descriptions name a must-block
  threat in one column, most of them a vertical three** (e.g. rank 6 L4 N254+: "the opponent has three stones stacked vertically at the
  top of column 0"; rank 13 L5 N635+; rank 22 L5 N366-). 10 of the 120 programs reach tactic agreement >= 0.5; 7 of those 10 are
  circuit neurons. Descriptive note: a column-specific *vertical* block detector agrees only partly with block_now_c (which also counts
  horizontal and diagonal threats), so tactic agreement understates such descriptions (rank 5: agreement 0.41); the registered measure
  is kept unchanged for Test B.
- Test B units (`scripts/37_ns3_prepare.py`, `configs/ns3.yaml`): 50 = top 20 circuit poles + 20 matched decoys (median match
  distance 0.17 in standardised log-magnitude / kurtosis) + 10 random directions, ids U01-U50. Membership file
  `results/ns3_membership.json` (sha256 5dbd555c1135558e…) is kept out of git and out of the bundle until Test B returns.
- Bundle `build/ns3_bundle.tgz` (sha256 a8a5e2005abffad3…; `scripts/38_ns3_bundle.py`): 20 files listed with hashes in ns3/BUNDLE_FILES.txt;
  no PLAN/LOG/results/ns/ns2/validation data/circuit code; the shipped config is cleaned and every text file is checked for
  design words. Checked in a fresh folder on the pod: units, examples, facts and score all run without the held-out data.
- Pod terminated after the pull. Spend this session about $0.35 (≈20 min).

## 2026-11-23 — Horizontal / diagonal blocking: neurons vs directions (PLAN addendum t)

Pod c4-orient (Secure RTX 4090; waited ~17 min for placement before SSH came up), tests 5/5, full run 395 s, pulled, terminated.
`results/orientation_followup.json`. Pairs per orientation (discovery / confirmation): vertical 4,000 / 4,000, horizontal 3,253 / 3,281,
diagonal 3,123 / 3,160. Ceiling E_all (all 5,120 neurons of layers 0-4) 0.99 in every orientation; target 0.8 x E_all.

| layers 0-4 | N80 neurons (confirm) | D80 directions (confirm) | N80/D80 | random subspaces p95 | top head (val) | top-4 heads |
|---|---|---|---|---|---|---|
| vertical | 3,000 (0.79) | 15 = 3/layer (0.83) | 200 | 0.5% | L0 H2 0.44 | 0.93 |
| horizontal | 290 (0.79) | 40 = 8/layer (0.81) | 7.3 | 0.9% | L0 H2 0.18 | 0.79 |
| diagonal | 770 (0.80) | 60 = 12/layer (0.89) | 12.8 | 0.9% | L0 H2 0.07 | 0.22 |

All layers (secondary): D80 = 18 / 48 / 72 directions (confirm 0.86 / 0.85 / 0.92); the (s) neuron circuit for vertical threats over all
layers was 53 neurons.
- (t-1) FAILED, in the opposite direction: upstream of layer 5, vertical blocking needs the MOST neurons (3,000), horizontal the fewest (290).
- (t-2) FAILED: D80 <= 30 holds for vertical (15) only; horizontal 40, diagonal 60 (both confirm >= 0.75 x E_all).
- (t-3) FAILED, opposite: N80/D80 is largest for vertical (200) and smaller for horizontal (7) and diagonal (13).
- (t-4) held: random subspaces of the same size remove <= 1%.
- (t-5) FAILED, opposite: the top head effect is largest for vertical (L0 H2 44%), then horizontal (18%), diagonal (7%).
Reading (the registered readings did not anticipate this pattern; stated as an interpretation, not a test): vertical blocking is the
*simplest* computation in direction terms (15 directions, one head carries 44%), but upstream of layer 5 it is the least neuron-aligned:
its few directions are spread over thousands of neurons. The compact 53-neuron vertical circuit of (s) must therefore sit mostly in layer 5
(the best 50 neurons of layers 0-4 remove only 23% of the vertical gap; its layer list was not saved in (s)),
next to the readout (column-specific "threat in column c" neurons), with a distributed low-dimensional code feeding it. Horizontal and
diagonal threats need more directions and are more neuron-aligned upstream (fewer neurons per direction). Caveat on the descriptive
participation ratios (medians 1-49 neurons per direction): a ratio near 4 can still leave half of a direction's mass spread over
hundreds of neurons, so they understate the spread; a mass-coverage measure would be clearer (not computed).

**Limitation recorded (2026-11-23, user decision).** The neuron-first method (rank single neurons, keep the smallest set that carries
the behaviour, then describe each neuron) works when a few neurons do most of the work: vertical blocking, whose last step is a set of
column-specific layer-5 neurons (53 neurons carry 80%, and Test A's descriptions name them). It is not the right tool for horizontal and
diagonal blocking, where 200 neurons are not enough over all layers, 290 / 770 are needed upstream, and the computation is better
described by 40 / 60 directions spread over many neurons. A horizontal Test B was considered and not run. Next: map the vertical blocker
end to end (addendum u) and build its demo.

## 2026-11-23 — The vertical blocker end to end (PLAN addendum u) and its demo

Pod c4-vertical (Secure RTX 4090 after Secure/Community 4090 and A4500 had no capacity; flaky SSH, so the job ran detached), tests 5/5,
full run 41 s; `results/vertical_map.json`. Pulled, terminated.
- The (s) rule on the vertical pairs reproduces **V = 53 neurons** (layers 0: 8, 2: 5, 4: 4, 5: 36; confirmation effect 79%). R = the 36
  layer-5 neurons; R alone removes 79% of the gap; the 15 directions (3 per layer, layers 0-4) 81%.
- (u-1) FAILED: L0 H2 puts 24% of its last-position attention on earlier same-column moves (uniform 17%).
- (u-2) held: patching the 15 directions moves R by 94% of its clean-minus-corrupted change.
- (u-3) held: 92% of R promote the block column they matter most for (column alarms).
- (u-4) FAILED: first directions vs the opponent's run on the last-move column, Spearman 0.07, -0.31, 0.08, 0.03, 0.09.
- (u-5) mean-ablation at every position, 8,046 vertical / 5,027 horizontal / 5,942 diagonal must-blocks and 3,000 control positions
  (intact: 99.9 / 94.9 / 94.5 / 94.8%). (i) held: head off → vertical 72.8%, control 90.4%. (ii) FAILED narrowly: directions off →
  vertical 64.4% (−35), control 83.6% (−11, bar 10). (iii) FAILED: readout off → vertical 69.8% (−30), control 80.4% (−14, bar 5).
  Random controls of the same size: 0 points. Horizontal/diagonal blocks barely move under the head or readout switch (−1 to −3).
- Post-hoc, descriptive (`scripts/40b_vertical_posthoc.py`, `results/vertical_posthoc.json`): L0 H2 is an "opponent's recent moves"
  head: 65% of its attention goes to the last mover's earlier moves in any column (14% and 12% to their latest two); same-column share
  rises from 9% on ordinary positions to 23% on vertical threats because the stack is made of those recent moves. The first direction of
  layers 1, 2, 4 detects "vertical threat on the last-move column" with AUROC 0.76-0.78 (base rate 5.9%); layers 0 and 3 near 0.5.
- Demo `docs/blog/vertical/` (draft): live model with the three switches (`switches.js`, shared with `tests/check_vertical_port.js`;
  max logit difference to PyTorch 4.5e-5 under every switch), attention rings, direction tubes, column-alarm lamps, move bars; text
  states the failed predictions and labels the post-hoc readings. Data from `scripts/41_vertical_demo_export.py`. Bug found in the
  browser: softmax on a Float32Array turned the bar markup into NaN (fixed with Array.from).

## 2026-11-23 — Blog post draft (docs/blog/post/)

Draft "Watching a Small AI Block a Threat in Connect Four" (title is a proposal). Main story: model (01), board in its head (02), the
vertical blocker with the live demo embedded (03), would an agent have found it (04, Test A; Test B pending), limits (05); appendices
A training, B size ladder, C what worked / didn't, D horizontal and diagonal, E other concepts, F honesty measures. Built by
`scripts/42_build_post.py` from result files only (101 values, figures in data/figures.js); checks: ladder correlation recomputed from
the 43 runs (0.966), the frozen circuit hash is in this log, the vertical circuit reproduces, agent-study totals (44, 9), and the wording
"every description names a threat" is asserted. Citations (7) verified against their arXiv / Goodfire pages. QA: no console errors,
no overflow at 375px, every cite resolves and every reference is cited. The demo's vertical.js now tolerates missing page elements so it
can be embedded. Placeholders left: [author], [link]. Not published.
- 2026-11-23, revision at the author's request: main text cut from ~1,750 to ~1,200 words (model and board merged into one section;
  method detail and the failed-prediction details moved to Appendix B; the full agent-description table moved to Appendix G, the main
  text shows the three highest-ranked circuit neurons as one-line excerpts); new section 05 "What comes next: mapping other concepts".
  Appendices now A-H. Floating contents list (desktop rail, phone button) confirmed. QA repeated: no errors, no overflow at 375px.
- 2026-11-23, redesign at the author's request ("the visualization is the star"; "be innovative"; "show the neuron atlas through
  the blog"): the post is now a scrolling story. A dark stage stays pinned beside nine story cards (on phones, pinned at the top): the
  live board (fixed colours: reader ochre, model blue, `VDEMO_FIXED`), the model's four steps, the switches, and a live map of all 6,144
  neurons (six 32x32 layer blocks, neurons grouped by best-matching concept family, brightness = activation relative to each pole's
  firing threshold; hover or tap for the neuron's concept, roles and the agent's description). Each card sets the position, switches
  and which neurons the map highlights (cells, the circuit, upstream circuit, the alarms, the agent-described ones). Map data:
  `scripts/43_atlas_map_export.py` (asserts the circuit and alarm counts; 9 described circuit neurons matched on pole, as in Test A).
  The demo script gained a driver API (`window.VDemo`) used by `docs/blog/post/story.js`. Concept text in the map is shown with columns
  and rows from 0, like the rest of the post. QA: no errors; stage fits a 900px window; no overflow at 375px.

## 2026-11-23 — Neuron atlas, three views (draft, docs/blog/neuron-atlas/)

Layers (6 x 1,024 grid by theme, agent-described, blocking circuit, or live board), Map (t-SNE of all 12,288 poles' board patterns,
`scripts/44_atlas_map_layout.py`, pod, seed 20261123, 18 regions), Library (agent-described / circuit / alarms / all, neuron pages
with board heatmaps, examples, column effects, tactic support, agent description, circuit role). Concept labels only (no agent labels
for all poles yet). **Bug found and fixed:** overview/L*.json concept indices refer to the full 681-name list, but the old atlas looked
them up in meta.json's filtered 659-name list, showing the wrong concept for 7,170 of 12,288 poles; old atlas patched (names.json),
new atlas uses the full list. Post links to the new atlas. NOT yet checked in the browser.

### 2026-11-24 Test B (S7) results returned; frozen before scoring
- `ns3_results.zip` (sha256 5f8c3658...118e7) from a separate Claude account: 50 of 50 units submitted, no re-runs, agent
  claude-opus-5-5 for every unit, bundle and prompt hashes matched. Copied unchanged into `ns3/descriptions/`, `ns3/work/`,
  `ns3/orchestrator_log.md` and committed before anything was scored.
- Orchestrator-logged rule breaks (local counting of a candidate rule on firing vs non-firing dev examples): U02, U08, U16, U21,
  U23, U26, U27, U30, U32, U37, U45, U48, U50 (13). Submissions untouched, as the protocol requires. Primary results use all 50 units;
  a labelled follow-up repeats them without the 13 (not registered).
- Text-only check pack (s-B2) exported blind from the descriptions alone (`scripts/45_ns3_textcheck.py export`, seed 20261124),
  before the answer key was opened; it runs on a separate Claude account.
- Scoring: `scripts/32_ns_verify.py run` (the (r) verification, unchanged) then `scripts/46_ns3_score.py` (S7 measures + unblinding).

### 2026-11-24 Test B (S7) results, unblinded (`results/ns3_testB.json`, `scripts/46_ns3_score.py`; verify log in runs/)
Validation split, 5,000 games, >= 4 stones; 20 circuit poles, 20 matched decoys, 10 random directions. Answer key
`results/ns3_membership.json` now committed. Pod: Secure 4090, about 1 h ($0.89/h), terminated after the pull.
- **(s-B1, headline) HOLDS.** Tactic agreement >= 0.5: circuit 14 of 20 (70%), decoys 2 of 20 (10%, exactly at the bar), random
  1 of 10. The 14 are all column-specific must-block detectors (layer 5 alarms, plus L4 N254+ and L2 N830+); agreement 0.50-0.96.
- **(s-B2) FAILS** on the decoy side. Text-only judge (fresh model, blind, separate account) says yes for 18 of 20 circuit poles (90%)
  and 6 of 20 decoys (30%; bar <= 10%). Decoys judged yes are mostly layer-5 tactical units (open three on the bottom row, a
  vertical three in column 5 (U19), the mover's own three), so the question is passed by tactical text in general, not only blocking.
- **(s-B3) HOLDS.** Held-out F1 against own firing (p97 / p3): circuit median 0.53, decoys 0.29, difference 0.25 [0.16, 0.33].
  Secondary thresholds (frozen programs re-scored): p90 +0.03 [-0.07, 0.08], p80 -0.02 [-0.09, 0.02]: the advantage is in the
  firing tail the agents were asked to describe, not in weaker activity.
- **(s-B4)** comparability with (r): real median F1 0.46 vs random 0.24; 60% of real units above the random p90 (0.38).
- Agent confidence separates the groups on its own: circuit 2 high / 17 medium / 1 low; decoys 2 / 2 / 16; random 0 / 1 / 9.
- The 6 circuit poles under 0.5: two layer-0 neurons described exactly (F1 0.95, 0.90) as "the opponent's last stone landed in
  column 4 / is the first stone in column 5" (the inputs of the circuit, not a tactic; consistent with the (u) post hoc reading of
  L0 H2); two vertical-three-in-one-column descriptions just under the bar (0.48, 0.46: the program covers vertical threats only,
  the concept includes horizontal and diagonal blocks in that column); two non-vertical units (horizontal threats on the bottom row).
- Follow-up, not registered (without the 13 logged rule breaks): circuit 13 of 18 (72%), decoys 2 of 16 (12.5%, so s-B1 would
  narrowly miss on the smaller denominator; both decoys over the bar are not rule breakers); s-B3 +0.23 [0.15, 0.37]; text-only
  circuit 89%, decoys 31%. The conclusions do not depend on the rule breaks.
Reading (per the pre-registered outcomes): (s-1) failed narrowly, so S7 is a test on "the most important neurons" (top 20 of C by
exact effect). On those, the blind describing agent, not told about blocking, wrote a block-in-column-X description that predicts
the block concept for 14 of 20, against 2 of 20 matched decoys: the first validated case for the method in this project, limited to
the vertical/column alarms that make up most of the top 20.
- Post and atlas updated with Test B (2026-11-24): step 02.5 rewritten around the blind test, new Figure 4 (tactic agreement strip,
  circuit / decoys / random, registered bar), a Limits bullet for the failed text-only check, Appendix I (design, the three tests,
  misses, rule breaks, all 50 units unblinded); appendix figures renumbered 5-6. `scripts/42_build_post.py` asserts the counts against
  `results/ns3_testB.json` and that s-B1/s-B3 hold and s-B2 fails. Atlas: the 40 Test B neuron descriptions added to `ds`
  (`scripts/43_atlas_map_export.py`), every description of a pole shown on its page, new Library set "Blind test".
- 2026-11-24, post restructured (user request: the demo took over the page; link it, as Goodfire does). The live model, neuron map
  and guided tour moved to a companion page `docs/blog/post/demo/` (template `demo/demo.tpl.html`, also filled by
  `scripts/42_build_post.py`; asset paths set by `window.VDEMO_MODEL` / `window.ATLAS_URL`). The post is now a regular article: a
  demo card (screenshot `img/demo.png` + "Open the demo"), sections 01 board, 02 how it blocks (new Figure 2: the four-step circuit
  with each step's switched-off block rate), 03 the blind agent test, 04 limits, 05 next; figures renumbered 1-7. Phones: the tour's
  trigger band now sits below the pinned stage. Publishing must ship `post/demo/` with the post (it is a linked page, not an asset).

### 2026-11-24 Pre-publication pass (nothing made public)
- Redaction: 81 tracked files (agent prompts, work folders, orchestrator logs in ns/, ns2/, ns3/) contained absolute home-folder
  paths of the machine the agent studies ran on; replaced with `{REPO}` / `{STUDY_DIR}`. Content otherwise unchanged. Hashes recorded
  earlier for those files (e.g. the returned zip) refer to the unredacted versions, kept in this private repository's history.
  The Test B unit prompt is unaffected (sha256 still 6477e18a...). `scripts/38_ns3_bundle.py` now redacts with a pattern.
- `scripts/make_public_snapshot.sh`: builds a public copy with fresh history (one commit from HEAD, no remote; refuses if any
  home-folder path is tracked). The private history keeps the unredacted paths, so the private repo itself should not be made public.
- References: all six arXiv titles and authors confirmed against the arXiv API; the Goodfire page title, authors and date confirmed.
- Post: Appendix F's link to the old agent atlas (docs/blog/ns-atlas/, a superseded draft) now points to the neuron atlas library.
- Publishing: `scripts/47_publish_bundle.py` assembles post + demo + atlas (with run-time files listed in publish-files.txt) into
  build/publish_post/ (30 files, 23.6 MB). The site publisher was extended (site branch `blog-connect4-pages`, local commit e3edbf6,
  not pushed) to copy linked local pages and listed run-time files; an existing post's dry run shows no changes. Staged as slug
  `connect-four-blocking` (provisional) and checked in the browser: post (7 charts, demo card), demo (model loads, tour works), atlas
  (neuron pages, live board), no console errors.
- README rewritten for the finished project; REPRODUCE.md gains a table of every later study. Tests: 22 passed; JS port check passes.
- 2026-11-24: title "Can an AI Agent Find the Neurons That Block a Connect Four Threat?" (author's choice), slug connect-four-blocking-neurons; draft labels removed; share-card colours set. Staged on site branch blog-connect4-pages, not pushed.
- 2026-11-24: post section 04 "What we take away" (two takeaways + comparison table with Tigges et al.; their conclusion is broader, ours conditional); Limits/Next renumbered 05/06; .tscroll restored in post.css.
- 2026-11-24 PUBLISHED : https://mayank26saxena.github.io/blog/connect-four-blocking-neurons/ (site commit 4ce43cc, rebased on two newer site commits). Verified live: post (7 charts, demo card, comparison table), demo (model loads, tour drives the board), atlas (neuron pages); all files 200; no console errors. Research repo stays private, so the post's code link returns 404 until it is made public.
- 2026-11-24: section 04 comparison removed (author's request); one takeaway paragraph in section 03; prior work cited once as context. Notebook and plan wording made neutral (no account balances or assistant-style phrasing; substance unchanged). Public code lives in a separate fresh-history repository, mayank26saxena/connect-four-neurons; this repository stays private.
- 2026-11-24: public repository created: https://github.com/mayank26saxena/connect-four-neurons (fresh history, snapshot of bcf99e6, commit 1370ce6); post's "Code and data" now links there (site 2057588).
- 2026-11-24: title changed to "An AI Agent Found Most of the Neurons That Block a Connect Four Threat" (author's choice; not a question); slug unchanged.
- 2026-11-24: neuron atlas gets "How to read this page" guides (Layers, Map, Library, every neuron page), open by default, closed state remembered per browser.
