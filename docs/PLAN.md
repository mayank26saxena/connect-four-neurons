# Neurons as an interpretable basis, in a model that plays Connect Four

Plan and pre-registration. Written 2026-11-18, before any model was trained.
Deviations from this plan are recorded as dated addenda at the bottom; the plan text above them is not edited.

## 1. Question

Goodfire's *Neurons as an Interpretable Basis* (Tigges et al., Nov 2026) argues that raw SwiGLU MLP neurons in a
large language model are a usable unit of analysis: they are functionally sparse, each pole (positive or negative
extreme) usually has one dominant mode, and natural-language descriptions of poles predict their activity. Those
claims were evaluated without ground truth: descriptions were scored by an LLM judge against text.

This project repeats the analysis in a setting where the true concepts are known. A small transformer with the
same MLP design (bias-free SwiGLU) is trained to play Connect Four from the raw move sequence. Every position can be
labelled exactly by a rules engine (threats, forced blocks, immediate wins, board cells), so we can ask:

- **Q1 Sparsity.** Is the model functionally sparse in the same way? How much of each neuron's activation range can
  be zeroed before play degrades?
- **Q2 Poles.** Do the positive and negative extremes of a neuron mean unrelated things?
- **Q3 Concepts.** What fraction of poles match a single ground-truth concept, and how well?
- **Q4 Modes.** For poles that do not, do their firings split into a small number of modes, and does one mode carry
  most of the causal damage?
- **Q5 Action.** Do the concept-matched poles cause the behaviour their concept implies (for example, does ablating a
  "must block column c" pole stop the model from blocking)?
- **Q6 Formation.** When during training does each concept get a neuron, relative to when the model starts acting on it?

The output is a reproducible repository and a blog post with a live, in-browser demo: play against the model and
watch which neurons fire, what they encode and what happens to the model's move when you switch them off.

## 2. Setup

### 2.1 Game engine and teacher
- C bitboard engine (`engine/c4.c`, loaded with `ctypes`): legal moves, play, win check, threat maps.
- Teacher: deterministic negamax with alpha-beta, transposition table and a threat-count leaf heuristic, searched to a
  fixed depth (no time limits, so output is identical on every machine). Exact wins and losses inside the horizon
  are scored as such.
- Policy target for each position: softmax over legal moves of teacher scores at temperature T.

### 2.2 Data
- Games are played by the teacher, sampling from its softmax, with the first k plies random for opening diversity.
- Splits are generated from disjoint seeds: train, validation, analysis (held out; all neuron analysis uses it).
- Every position also stores its concept labels (section 2.4) for the analysis split.

### 2.3 Model
- Decoder-only transformer over move tokens (7 column tokens + BOS), context 43.
- Planned size: 6 layers, d_model 256, 8 heads, SwiGLU MLP with d_ff 1024 (6,144 neurons), RMSNorm, learned
  positions, no biases. About 6M parameters, small enough to run in the browser.
- Loss: cross-entropy against the teacher's soft target at each position. Illegal moves are never in the target;
  the model must learn legality from the sequence.
- Checkpoints saved on a log-spaced schedule for Q6.
- Training is small enough for a single Apple-silicon laptop (MPS); a cloud GPU is only needed if the pilot shows
  the model needs to be larger.

### 2.4 Ground-truth concepts
Computed by the engine for the position after each token, from the perspective of the player to move:
- board cells: mine / theirs / empty for each of 42 cells; landing cell for each column; column full
- immediate win available in column c; opponent threatens to win in column c (must block)
- threat cells (a cell that would complete four) for each side, playable or not; odd/even-row threats
- double threat (two immediate wins) for each side; "poisoned" column (playing it lets the opponent win above)
- last move: column, whether it created a threat, whether it blocked one
- game phase (ply), teacher evaluation (winning / losing / level)

### 2.5 Neuron definitions (following the post)
- Activation of neuron n: a = SiLU(w_gate·x) × (w_up·x). Each neuron has two poles: positive and negative.
- Percentiles are per neuron over the analysis split. A pole "fires" above its p97 (positive) or below its p3
  (negative), matching the post's p97/3 convention; we also report p99/1.
- Quadrants: sign of gate pre-activation × sign of up projection.

## 3. Analyses and metrics

| Q | Method | Main metric |
|---|---|---|
| Q1 | Zero activations inside per-neuron percentile bands (P25–75, P10–90, P5–95, P3–97, P1–99), plus top-k per layer; random-k and bottom-k baselines | KL to the intact model; agreement with teacher's best move; win rate against the teacher |
| Q2 | Compare the concept profiles of the two poles of each neuron | correlation of concept associations between poles |
| Q3 | For each pole and each binary concept, precision, recall and F1 of "pole fires" against "concept true"; AUROC of the raw activation | share of poles with best-concept F1 ≥ 0.8 (and ≥ 0.5) |
| Q4 | Cluster a pole's firings by upstream attribution (direct-path contributions from earlier neurons and attention) with Leiden on a kNN graph; ablate the pole per mode | modes per pole; share of poles whose top mode carries ≥ 90% of KL damage |
| Q5 | Ablate or clamp a concept-matched pole and measure the behaviour its concept predicts (block rate, win-taking rate, cell-specific play) | change in behaviour rate versus random-pole ablations |
| Q6 | Repeat Q3 and play-strength metrics on each checkpoint | step at which each concept's best pole reaches F1 0.8 versus step at which the matching behaviour reaches 90% |

Random-direction baseline: Q3 is repeated on random rotations of each MLP layer's activation space. If neurons are a
privileged basis, their best-concept F1 should exceed that of random directions.

Optional: LLM-written pole descriptions scored against ground truth (detection accuracy). This needs an API key and
is packaged as a separate, cached script; it is not required for any headline number.

## 4. Pre-registered expectations

Stated before training, to be checked, not assumed:
- E1: zeroing the P5–P95 band costs less than 5 percentage points of agreement with the teacher.
- E2: at least 30% of poles in layers 2–6 have a best-concept F1 ≥ 0.5, and neurons beat random directions on this
  metric.
- E3: the median pole has one dominant mode.
- E4: threat and must-block concepts get dedicated poles before the model reliably blocks.

## 5. Deliverables

- `engine/` C engine and Python bindings; `c4n/` package (data, model, training, analysis); `scripts/` one entry
  point per stage; `configs/` all hyperparameters.
- `results/` JSON tables, one per analysis, written only by scripts. Every number in the post comes from them.
- `web/` the live demo: a plain JavaScript forward pass of the trained model (weights exported from the final
  checkpoint and checked against PyTorch to a stated tolerance), with neuron readout and ablation.
- `docs/blog/` the post, built from `results/` by an export script and published to the blog with the shared style.
- `REPRODUCE.md`, pinned environment (`uv.lock`), seeds in configs, `MANIFEST.sha256` of data and checkpoints,
  and a single `make all` that rebuilds everything from scratch.

## 6. Addenda

**2026-11-18 (a), before training.** Compute: all stages run on a single NVIDIA RTX 4090 host instead of the
Apple-silicon machine mentioned in 2.3. No change to the model, data or analyses.

**2026-11-18 (b), before training.** Q4 implementation detail fixed in advance: subcircuits are Leiden clusters of a
pole's firings on exact upstream-attribution vectors; modes are subcircuits merged when their ground-truth concept-rate
profiles correlate above 0.8 (`configs/base.yaml: modes`). This replaces the LLM judge used by Tigges et al. Q3
results will be reported by concept family, because a smoke run showed that game-phase and single-cell concepts
(available from positional and token embeddings) dominate the raw ranking.

**2026-11-19 (c), after the main run, before the sweep.** The main run (d_ff 1,024) did not reproduce functional
sparsity or a neuron advantage over random directions. Tigges et al. studied a model with ~5M neurons; ours has 6,144.
A width sweep tests whether the neuron-basis properties depend on the number of neurons per layer relative to the
residual width (superposition pressure falls as d_ff / d_model grows).

Design: d_ff in {256, 512, 1,024, 2,048, 4,096} (d_ff / d_model = 1 to 16), two training seeds each (10 runs), all
else identical to the main run, same data (`scripts/make_sweep.py`). Every run gets Q1, Q3, Q4, Q5 and Q5b
(group ablation, below). Concept vocabulary extended before the sweep with the 69 four-cell lines (an open two or
open three of either side: 276 concepts), so that poles tracking line segments are not scored as unmatched.

Predictions (direction only; tested as a monotone trend over the five widths, seeds averaged):
- W1: the agreement cost of zeroing P5–P95 falls as d_ff grows.
- W2: the neuron-minus-rotation difference in the share of poles with tail-threshold F1 >= 0.5 rises with d_ff and
  is positive at d_ff = 4,096.
- W3: the share of poles whose top mode carries >= 90% of damage rises with d_ff.
- W4 (main model): zeroing the top-k poles for a concept lowers the matching behaviour more than k random neurons from
  the same layers, for k >= 10.

**2026-11-19 (d), before any SAE result.** Q7 added: neurons versus a TopK sparse autoencoder per layer (4,096 latents,
k = 32, trained on 20,000 training-split games), scored against the same ground-truth vocabulary with the same
F1 procedure (`scripts/11_sae.py`). Tigges et al. argue for neurons over learned dictionaries; the ground truth lets us
compare the two directly. Prediction S1 (stated without a strong prior): SAE latents have a higher share of units with
tail-threshold F1 >= 0.5 than neuron poles in the main model. FVU is reported alongside, since a dictionary can buy
monosemanticity by dropping variance.

**2026-11-21 (e), before any of the tests below were run. Validity tests.** The results so far leave six weaknesses that could
change the conclusion:
1. *Selection bias.* A pole's "match" is the best of 659 concepts x 6 thresholds on the same data used to score it; chance
   inflates both bases, and not necessarily equally.
2. *Vocabulary dependence.* "Neurons are no better than random directions" is measured only against our concept list. A
   vocabulary-free test of whether the neuron basis is special is missing.
3. *Two seeds* per width, and no intervals anywhere.
4. *Training length.* F1 of some neurons was still rising at step 8,000; the models may be under-trained.
5. *Weight decay* is one fixed value (0.1); privileged bases are often attributed to regularisation.
6. *Width confound.* Sweeping d_ff at fixed d_model changes d_ff / d_model together with absolute width.

Tests (all on the final checkpoints; "gap" = share of poles matching a concept (F1 >= 0.5, tail sweep) for neurons minus
random rotations, as in the width sweep):
- **T1 basis privilege, vocabulary-free** (`13_basis_controls.py`). Mean excess kurtosis of the per-unit activation
  distribution, and the share of squared activation held by the largest 5% of entries, in the neuron basis vs 3 random
  orthogonal rotations. Prediction: neurons have higher kurtosis than rotations in every model. A rotation of a heavy-tailed
  basis tends toward Gaussian, so if this fails the neuron basis is not special at all.
- **T2 sparsity relative to a rotated basis** (same script). Agreement lost by zeroing each unit's central 50 / 80 / 90% band,
  and by keeping only the largest 6.25% of units, in the neuron basis vs rotated bases at equal nominal fractions.
  Prediction: neurons lose less than rotations in every model, even though absolute sparsity is poor (E1).
- **T3 cross-fitted matching with intervals** (`14_crossfit.py`). Choose each pole's concept and threshold on half of the
  games, score it on the other half (and the reverse), 500 game-level bootstrap resamples, paired between bases.
  Prediction: held-out gap is negative at widths >= 1,024 with the 95% interval excluding zero, and neurons still win on
  open lines, landing cells and board cells.
- **T4 more seeds.** Seeds 3 and 4 at 256 and 1,024 neurons, seed 3 at 4,096 (three or four seeds per width, paired by seed).
  Prediction: gap(256) > gap(4,096) for every paired seed.
- **T5 training length.** d_ff 1,024 trained for 32,000 steps (4x) vs 8,000. Prediction: not an under-training artefact:
  |change in gap| < 2 points and the one-dominant-mode share moves by < 5 points.
- **T6 weight decay.** d_ff 1,024 with weight decay 0 and 1.0 (main runs use 0.1). No directional prediction; if the gap
  moves by more than 3 points, the result depends on regularisation and the post says so.
- **T7 ratio vs absolute width.** d_model 512 with d_ff 1,024 and 2,048, against d_model 256 with d_ff 1,024. Prediction: the
  gap depends on d_ff / d_model: gap(512, 1,024; ratio 2) > gap(256, 1,024; ratio 4), and gap(512, 2,048; ratio 4) is within 2
  points of gap(256, 1,024).

How the results will be read. T1 and T2 decide whether the neuron basis is special in itself: both hold means "special in
shape and function, but not aligned with our concepts", one fails means "not special". T3 decides whether the matching result
is real after removing selection bias. T4 to T7 decide whether the width trend is robust (seeds, training length, weight decay,
ratio). The post's claims are limited to what survives all of them; anything that does not is reported as not established.

**2026-11-21 (f), before the tactic analyses ran. End goal: which part of the model learns which tactic.**
Tactics are defined as labelled decision problems in `c4n/tactics.py` (verified against a brute-force board simulation,
`tests/test_tactics.py`): *win* (a winning move exists), *block* (no win, one forced block), *poison* (avoid a column that lets
the opponent win on top), *fork* (make two playable winning cells). Rate = share of positions where the model's greedy legal
move is correct. Tools (`scripts/16_tactic_atlas.py`):
- **Component necessity.** Mean-ablate each layer's MLP and each of the 48 attention heads; the drop in rate localises the
  tactic. Mean ablation (replace by the average over data) avoids the damage zero ablation does by itself.
- **Neuron attribution.** First-order effect of zeroing each neuron on the tactic's log-odds margin, summed over positions;
  validated by zeroing the top-k supporting neurons against k random neurons from the same layers (3 draws).
- **Decodability.** Linear probes on the residual stream after the embeddings and after each block, held-out by game.
- **Attention profile.** Average attention from the deciding position, by offset and to the start token, for every head.
Predictions: (P-a) every tactic depends on more than one layer, with MLPs in layers 3 to 5 or attention in layers 1 to 4
carrying most of the drop; (P-b) for each tactic the top-50 attribution neurons lower the rate more than 50 random neurons
from the same layers; (P-c) the tactic's information is linearly decodable one or more layers before the layers whose
ablation hurts the behaviour most; (P-d) win and block rely on a small set of heads (at most 6 of 48 account for half of the
total head effect); fork, the hardest tactic, is learned last in training and depends on more layers than win and block.

**2026-11-21 (g), deviation from (e) T4, decided after T1-T3 results and to save compute.** The third seed at 4,096 neurons
(about 45 GPU-minutes) was dropped: T4 is evaluated on paired seeds 1 and 2 at all widths, plus seeds 3 and 4 at 256 and 1,024
neurons. Reason: both existing seeds at 4,096 give a clearly negative gap (-5.3 and -3.9 points, cross-fitted intervals
excluding zero), so a third seed could not change the sign of the claim.

**2026-11-21 (h), before any world-model analysis ran. Does the model keep a board in its head, and do tactics read it?**
Motivated by Othello-GPT (Li et al. 2023, "Emergent World Representations"; Nanda 2023, "Actually, Othello-GPT Has A Linear
Emergent World Representation"). The model only ever sees column numbers; the board is never given to it. Tools
(`c4n/worldmodel.py`, `scripts/21_world_model.py`), on the analysis split, probes fitted on 70% of games and scored on the rest:
- **W1 Board probes.** At 13 read points (after the embeddings, after each attention sublayer, after each block), a
  multinomial linear probe per cell (42 cells x 3 states), in two framings: *relative* (empty / mine / theirs, mine = the
  player to move) and *absolute* (empty / first player / second player). Also a 1-hidden-layer MLP probe (relative), and the
  same linear probe on the untrained checkpoint (step 0). Baseline: the per-cell majority state given the move number.
  Reported: accuracy over all cells, emptiness accuracy (empty vs occupied), colour accuracy (on occupied cells).
- **W2 Derived board features.** Linear probes for each cell being a winning cell for the mover / the opponent (AUROC).
- **W3 Editing the board in the model's head.** At the last position, change the probe's reading of one cell by moving the
  residual stream along (w_target - w_source) until the probe's margin equals that cell's median held-out margin, at every
  block output from layer L on (L = 0..5), and see whether the model's move follows the *edited* board. Edits: flip the colour
  of one existing stone (headline); remove the top stone of a column; add a stone on a landing cell (secondary). Ground truth:
  the depth-10 teacher run on the edited bitboard with the same player to move. Scored edits are those where the model's clean
  move is a teacher-best move of the real board and the teacher-best sets of the real and edited boards do not overlap, so
  following the edit requires changing the move. Follow rate = share where the edited model's greedy legal move is
  teacher-best on the edited board. Controls: no edit, and a random direction with the same norm at the same layers. The
  start layer L is chosen on one half of the edits and the follow rate reported on the other half. Preservation: on edits
  that do not change the teacher-best set, the share where the edited model's move stays teacher-best.
- **W4 Who builds the board.** Mean-ablate each of the 48 heads and measure the drop in colour and emptiness accuracy of the
  relative probe at the best read point; for each head, attention share on the mover's own past moves, the opponent's past
  moves and the start token.
- **W5 Neurons in board terms.** For every neuron, cosine of its effective input weights (gate row times the RMSNorm gain) with
  the probe directions at the read point before its MLP (mine-minus-theirs and empty-minus-occupied per cell), and of its output
  weights with the probe and threat-cell directions after its block. Exported to the atlas as 6x7 maps.
- **W6 Emergence.** W1 (relative, block outputs) for each emergence checkpoint.
Predictions: (W-a) relative framing: colour accuracy at the best read point >= 95% and overall >= 98%; the absolute linear
probe's colour accuracy is lower by >= 5 points at that point. (W-b) the untrained model's best colour accuracy is >= 10 points
lower. (W-c) on held-out colour-flip edits, the follow rate at the chosen start layer is >= 50%, and >= 30 points above the
random-direction control. (W-d) preservation >= 80%. (W-e) the 3 heads whose ablation lowers colour accuracy most are all in
layers 0 to 2. (W-f) the top-50 block-attribution neurons (from 16_tactic_atlas) have a larger median max-|cosine| between
their output weights and the opponent-threat directions than random neurons from the same layers (permutation p < 0.05);
likewise top-50 win neurons with the mover-threat directions.

**2026-11-21 (i), after W1-W5 results and before running it. Exploratory follow-up to the failed edit test (W-c).** Observed:
W-c failed (held-out colour-flip follow rate 15.6% against 10.9% for a random direction of the same norm; preservation 94%).
Three explanations, each with a test (`scripts/21b_edit_followup.py`, same edits, same selection/report split by game):
- **Too weak.** Multiply each target margin by k in {1, 2, 4, 8}.
- **Wrong place.** Edit at every read point from point p0 on (p0 in {1, 3, 5}: after L0, L1, L2 attention), not only at block
  outputs. The board is read best after attention sublayers (W1).
- **Wrong variable.** The move may read *threat cells* rather than stones. Threat edit: for every cell whose mover / opponent
  threat label differs between the real and the edited board, set that threat probe's logit to the median held-out logit of
  its new label, at every read point from p0 on.
The schedule and strength are chosen on the selection half; reported on the other half, always with a same-norm random control.
Predictions, stated as the bar for "the model's move uses this representation": (i-a) the best board-edit schedule reaches a
follow rate >= 50% on colour flips and >= 30 points above its random control; (i-b) the threat edit reaches >= 50% on edits that
create or remove an immediate threat, >= 30 points above its random control. If neither holds, the post says the probes find a
board the model encodes but we could not show it is the variable the move is computed from.

**2026-11-21 (j), before running. Is the board used? Edits at every position where the stone is visible.**
The failed edit tests (h, i) rewrote the belief at the *current* position only. Later layers can still read the true board
from earlier positions through attention, so a current-position edit may be overruled. `scripts/21c_edit_history.py` repeats
the colour-flip test (same edits, same selection/report split by game, flips only) with:
- **Scope.** *current* (as before), *history* (every position from the one after the stone was played up to, but not including,
  the current one), *all* (history plus current). The relative label of a stone alternates with the mover, so the edit swaps
  mine/theirs at each position.
- **Direction.** *probe* (as in (h): along w_tgt - w_src until the probe margin equals k x the cell's median margin) and
  *meandiff* (k x the difference between the mean residual of cells in the target state and in the source state, per cell and
  read point, fitted on the training games). Mean difference is the standard check that a probe direction is not just a
  readout direction.
- **Start and strength.** Edits applied at every read point from p0 in {after L0 attention, after L1 attention} on;
  k in {1, 2, 4}. Always with a random direction of the same norm at the same positions.
The configuration is chosen on the selection half and scored on the report half. Guard: preservation (edits that do not change
the best move) must stay >= 70%, otherwise the edit is only breaking the model.
Prediction (j-a): the best *all* configuration reaches a follow rate >= 50% on the report half, >= 30 points above its random
control, with preservation >= 70%. Reading: if (j-a) holds, the move uses this board, and it reads it through earlier positions;
the gap between *current* and *all* says how much. If it fails, the post says the board is decodable and built by identifiable
heads, but linear edits (probe or mean-difference direction, at every position) do not steer the move.
(j-b): *history* alone beats *current* alone for the chosen configuration (the model reads the board from the past).

**2026-11-21 (k), before running. A treatment-versus-control experiment, replicated over small models.**
Why. Addenda (h)-(j) compare an edit with a random direction. That is a weak control: a big perturbation lands on a
teacher-best move of the edited board about 20% of the time by itself. A valid design holds the intervention fixed and varies
only whether the edited stone *matters*. Why small models. The 6-layer model may have several redundant routes to the move, so
one edit is overruled; a 3-layer model with d_model 128 (about 0.8M parameters) has fewer routes, trains in minutes, and
allows 5 independent seeds, so the unit of replication is the model.
Design (`scripts/22_board_causal.py`, per model, held-out games, game-level selection/report split as before).
- **Pairs.** For each position where the clean model plays a teacher-best move, pick (seeded) one *relevant* flip and one
  *irrelevant* flip of an existing stone, both at the same position. Relevant (treatment): the teacher-best set of the edited
  board does not overlap the original. Irrelevant (control): the two sets are identical. Positions without both are dropped.
- **Intervention.** Identical for both: rewrite the believed state of that one stone (mine <-> theirs) at every position from
  the one after it was played to the current one, at every read point from p0 on, along the probe or mean-difference
  direction, strength k (as in addendum (j)). p0 in {after L0 attention, after L1 attention}, direction in {probe, meandiff},
  k in {1, 2}. The configuration is chosen on the selection half by specificity (below) subject to the guard, then scored on
  the report half.
- **Outcome.** change = the edited model's greedy legal move differs from its clean move. *Specificity* = P(change | relevant)
  minus P(change | irrelevant), paired by position, with a 95% game-bootstrap interval (500 resamples). *Correct direction* =
  P(move in the edited board's best set | relevant, change). *Guard* = P(move still teacher-best | irrelevant) >= 0.70.
  Extra control: the same-norm random direction on the relevant flips.
Predictions. (k-a) Specificity >= 0.25 with the bootstrap interval excluding 0, and correct direction >= 0.5, in at least 4 of
5 small-model seeds. (k-b) The 6-layer model also reaches (k-a) (so the earlier ambiguity was the control, not the model).
(k-c) Mean specificity over small-model seeds exceeds the 6-layer model's (fewer redundant routes). Also reported: teacher
agreement and board-probe accuracy of every small model, since an edit test is only meaningful where the board is readable
(a model with colour accuracy < 90% at its best read point is reported but excluded from (k-a)).
Reading. (k-a) holds: the move uses the linear board, specifically; (k-b)/(k-c) say whether size matters. (k-a) fails with
readable boards: decodable but not used in this form, now with a valid control.
Small family: 3 layers, d_model 128, 4 heads, d_ff 512, 6,000 steps, otherwise the main recipe; seeds 1-5; same data splits.

**2026-11-21 (l), before the ladder ran, after the first small model (3 layers, d128, seed 1) gave specificity 0.23 (bar 0.25),
board colour accuracy 91.9%, teacher agreement 87.5%.** Goal: the smallest model for which the board test is clean, since a smaller
model is easier to understand. Ladder (`scripts/make_small.py --ladder`): layers x d_model in {1x64, 1x128, 2x64, 2x128, 3x64}
(4 heads, d_ff = 4 d_model, 6,000 steps, seeds 1-5; 3x128 is the small family of addendum k), each tested with
`scripts/22_board_causal.py`, aggregated by `scripts/23_ladder_summary.py`.
Predictions. (l-a) Teacher agreement rises with size and a 1-layer model plays clearly worse than a 3-layer one (>= 5 points).
(l-b) A 1-layer model has no readable board (colour accuracy < 90% at every read point), since the main model builds the
board over layers 0-2. (l-c) Every size with a readable board (colour >= 90% at its best point) and teacher agreement >= 80%
passes the board test (k-a: specificity >= 0.25 with interval above 0, correct direction >= 0.5, guard >= 0.70) in at least
4 of 5 seeds. The post reports the smallest such size ("the smallest clean model") and the full table, including sizes where
the test fails. Parameter counts are reported with every row.

**2026-11-21 (m), before the mid-size runs. Where between 0.8M and 6.3M parameters does the board test become clean?**
The ladder (l) found board colour accuracy and specificity rising together (Pearson 0.93 over 31 models), 0.21 at 3x128
(795k) and 0.40 at 6x256 (6.3M, one model). Sizes (heads of 32 dims, d_ff = 4 d_model, 6,000 steps, seeds 1-5 unless noted):
6x128 (4 heads, 2.2M), 4x192 (6 heads, 2.4M), 4x256 (8 heads, 4.2M); and 6x256 (8 heads, 6.3M) seeds 2 and 3 on the same
6,000-step recipe, to see whether the main model's pass replicates (the main model itself had 8,000 steps).
Predictions. (m-a) Specificity and board colour accuracy are monotone in parameters across 3x128, 6x128, 4x192, 4x256, 6x256
(Spearman of size means >= 0.9). (m-b) At least one of the three new sizes passes k-a (specificity >= 0.25 with interval above 0,
correct direction >= 0.5, guard >= 0.70) in at least 4 of 5 seeds; the smallest such size is reported as the smallest clean
model. (m-c) The two extra 6x256 seeds pass k-a. If (m-b) fails for all three, the post says a clean test needs more than
4.2M parameters in this recipe, which is not a small model.

**2026-11-21 (n), deviation from (m), decided after the 6x128 results.** 6x128 (1,581,952 parameters; (m) gave an estimate of 2.2M)
passed k-a in 4 of 5 seeds, which is (m-b). 4x192 (2,372,160 parameters) is larger, so no further size can be a *smaller* clean model.
4x256 (4.2M) was dropped to save compute (about 25 GPU-minutes); 4x192 and the two extra 6x256 seeds still run. Consequence:
(m-a) (monotone in size over five sizes) is evaluated on the sizes that ran.

**2026-11-21 (o), before running. Concept mapping in the smaller models (the goal of the project).**
Question: in the small models that pass the board test, how many of the 659 ground-truth concepts can be mapped to *one unit*
(a neuron pole) and how does that compare with random directions and with a supervised linear probe, against the 6x256 model?
Models: 4x192 seeds 1-3 (3,072 neurons), 6x128 seeds 1-2 (3,072 neurons), and the 6x256 main model (6,144). Retrained from
the same configs (the earlier checkpoints were not kept); each also gets the board test so concept mapping and causal
specificity are measured on the same model.
Measures (held-out, two folds by game as in the T3 cross-fit; concepts with >= 50 positive and >= 50 negative positions).
- **M1 (existing, `14_crossfit.py`).** Share of poles whose cross-fitted held-out F1 >= 0.5; neurons minus random rotations.
- **M2 (new, `24_concept_coverage.py`).** *Coverage*: the share of concepts whose best unit, chosen on one half of the games
  (any layer, either pole, tail threshold p90-p99.5), reaches held-out F1 >= 0.5 on the other half. Same procedure for random
  rotations of each layer (same number of candidate units) and for a linear probe on the residual stream (read point and
  probability threshold chosen on the first half; 7 read points in a 6-layer model). Game-bootstrap 95% intervals (500).
Predictions. (o-a) M1: the neuron-minus-rotation gap is <= 0 in at least 4 of 5 small models and none exceeds +1 point
(the sweep put d_ff 256 at +0.5 to +3.2 and d_ff 1,024 at -2.4 to -3.4 points; these have d_ff 512-768, narrow d_model).
(o-b) M2: probe coverage exceeds neuron coverage by at least 20 points in every model (directions map more concepts than
single units), and neuron coverage is at least rotation coverage by 5 points on the local families (cell, landing, threat,
last-move column) in at least 4 of 5 small models. (o-c) Board-cell concepts (126: mine / theirs / empty of 42 cells): probe
coverage >= 90% in the models that pass the board test; neuron coverage reported. (o-d) Neuron coverage of all concepts is higher
in the small models than in 6x256 (fewer units, less splitting of a concept across units). If (o-a)/(o-b) fail the post says so.

**2026-11-21 (p), deviation from (o), at the author's request.** The queue was stopped after seed 1 of 4x192 and 6x128 (checkpoints
and results kept in `checkpoints/concept/`, `results/concept/`); 4x192 seeds 2-3 and 6x128 seed 2 were not run. Reason: retraining
every seed was not needed to choose one model to study, and compute was limited. Consequence: (o-a)-(o-d) are evaluated on one seed
per small model, so the seed-to-seed spread of the concept-mapping measures is unknown.

**2026-11-21 (q), before any agent run. Agent-written, verified neuron descriptions ("Neuron Scientist"), after Goodfire.**
Goodfire (Tigges et al. 2026) had a frontier-model agent run experiments on each neuron pole (activations on chosen inputs,
steering, attribution), submit a description to a dev-set metric, revise for a fixed number of rounds, and then verified the final
descriptions on held-out data by detection (an LLM judge separates a firing from a non-firing snippet using only the description),
simulation (a reader predicts activation levels from the description; substituting them recovers a share of the zero-ablation
damage, KL) and input synthesis (beat the corpus maximum). Our version (`c4n/ns.py`, `scripts/30_ns_prepare.py`,
`31_ns_tool.py`, `32_ns_verify.py`, `docs/NEURON_SCIENTIST.md`) keeps all three and adds what Connect Four allows: each
description is written twice, in English and as a short program over the board, so detection can be scored exactly.
Design. Model: the 6x256 main model, loaded from the float16 web export (`web/model.bin`). Dev data: the analysis split
(5,000 games); the agent's tools read only this. Test data: the validation split (5,000 games), read only by verification.
Units: 70, blinded behind opaque ids: 20 poles the concept dictionary explains (in-sample best concept F1 >= 0.6), 40 it does
not (F1 < 0.3), 10 random directions of a layer's neuron space (a pseudo-neuron; the agent is not told which). Firing: beyond
the unit's own dev p97 (positive pole) or p3 (negative pole). Agent budget: at most 8 calls to the dev metric per unit.
Held-out measures per unit: (1) exact detection F1 and AUROC of the program; (2) simulation: replace the unit's activation by
the dev-mean activation of the program's level, KL recovery = 1 - KL(sim)/KL(zero), reported as a share of the ceiling of a
perfect 10-level reader; (3) input synthesis: does any submitted legal game beat the dev maximum; (4) text-only judge detection
(a fresh model sees only the English description and 20 firing / non-firing pairs). Baseline: the best of the 659 dictionary
concepts, chosen on dev, scored on test.
Predictions. (q-a) Unexplained stratum: median test F1 of the agent's program exceeds the dictionary baseline by >= 0.15.
(q-b) Explained stratum: agent median test F1 >= dictionary median - 0.05. (q-c) Random directions: median agent test F1 at
least 0.2 below the real units', and >= half of them get confidence "low". (q-d) Real units: median simulation share of ceiling
>= 0.5. (q-e) Real units: text-only judge accuracy >= 0.80 (chance 0.50). Reading: (q-a) and (q-c) together say the agent finds
real structure the dictionary misses without inventing it for noise; if (q-c) fails, every description is suspect.

**2026-11-21 (r), after (q) was verified and before any (r) agent run. Neuron Scientist follow-up: fixing the opening artefact.**
Result of (q), reported unchanged in `ns/report.md`: (q-a) holds (+0.16, CI 0.10-0.27), (q-b) holds, (q-c) FAILS (random-direction
median F1 0.58 vs 0.44 for real units; 5/10 rated low), (q-d) FAILS (median simulation share 0.12 with 3 undefined units skipped),
(q-e) holds (0.83) but random directions scored 0.84. Diagnosis, recorded before unblinding in `ns/orchestrator_log.md`: every game
starts from the same few positions and each one (empty board, each first move) is ~2.5% of all positions, close to the 3% firing
rate. Any direction whose value on one of them happens to be extreme fires there and gets an exact one-line rule (`ply == 0`):
3 of the 10 random directions were such empty-board detectors (F1 ~1.0, confidence high). (q) stands as run; (r) is a new study.
Design changes (config `configs/ns2.yaml`, workspace `ns2/`, code paths gated so (q) reproduces exactly):
(1) Positions with fewer than 4 stones (ply < 4) are ineligible: excluded from firing thresholds and dev maxima, from the agent's
examples and dev metric, from held-out detection and the dictionary baseline, and from judge pairs. Synthesis sequences must have
>= 4 stones. Simulation still replaces the unit at every position. (2) 30 random directions (5 per layer) instead of 10.
(3) Fresh units: 20 explained / 40 unexplained poles drawn with a new seed (20261122), excluding every neuron described in (q);
new random directions. (4) Synthesis sequences in which any move completes a four are rejected by the tools. (5) Medians skip
undefined (NaN) values and report how many were skipped. (6) One agent prompt from the start (`ns2/prompts/unit_prompt_r.txt`):
the (q) protocol plus the rules added during (q): `score` is the only measure of program quality (no local scorers, classifiers,
or counting how often candidate rules hold in firing vs non-firing examples; single-feature histograms are fine), legal unfinished
synthesis games, and a confidence rubric in which `high` also needs the rule to describe a board pattern, not a lookup of a few
specific openings or move sequences. Agent model, budget (8 dev-metric calls), firing percentile and all other settings as in (q).
Predictions, same tests and thresholds as (q) so the two studies compare: (r-a) unexplained: median agent test F1 - dictionary >= 0.15;
(r-b) explained: agent median >= dictionary median - 0.05; (r-c) random: median agent test F1 >= 0.2 below real units' and >= half
rated low; (r-d) real units: median simulation share of ceiling >= 0.5; (r-e) real units: text-only judge accuracy >= 0.80.
New: (r-f) at least half of the real units exceed the 90th percentile of the random directions' test F1. Expectations stated
now: (r-c) and (r-f) are the tests of the fix; (r-d) is expected to FAIL again (the 0-9 `level` reader in (q) recovered a median
12% of a perfect reader, a limit of the measure, not the artefact), and it is kept unchanged rather than lowered.
Reading: if (r-c) fails with openings excluded, agent descriptions are not distinguishable from noise directions in this model.

**2026-11-22 (s), before any computation. One tactic end to end: the blocking circuit, and a blind test of whether agent-written
neuron descriptions recover it.**
Why. Studies (q) and (r) scored agent descriptions against each unit's own firing. That shows a description predicts *when* a unit
is active, not that the agent found what *matters* for a behaviour. Here the mechanism of one behaviour is established first by
causal methods with exact labels, frozen, and only then are describing agents (blind to it) scored against it. The end goal is
an automated interpretability researcher; this study is its first validated case, so every step is a reusable module with a task
spec (`c4n/circuit.py`, `configs/circuit.yaml`), and a later task (win, fork, another model) re-uses the code with a new spec.
State of knowledge at registration (so later readers can judge bias). Read before writing this: the tactic atlas (block depends on
L0 H3 beyond the control; 42 of the top-50 block attribution neurons are in layer 5; zeroing the top 20 block neurons drops block
accuracy 0.91 -> 0.72 and forcing them on makes the model play that column 95%), (W5) block neurons' output weights are not more
aligned with opponent-threat probe directions than random, and the (q)/(r) descriptions. **Not looked at:** any overlap between
block-relevant neurons and the (q)/(r) units, any patching result, any receptive field. The circuit rule below is new and stricter
than the atlas attribution ranking, and its outcome is unknown.

S0. Behaviour, data, metric.
- Model: the 6x256 main model from the float16 web export (`ns.load_web_model`), the exact weights the agents use.
- Must-block position: the mover has no immediate win, exactly one legal column lands on an opponent winning cell
  (`tactics.tactic_masks`), at least 4 stones on the board, game not over. Correct move: that column.
- Behaviour metric: margin (log-sum-exp of the block column minus log-sum-exp of the other legal columns, `tactics.margin`);
  accuracy = the greedy move is the block column.
- Minimal pairs. Clean: a must-block position after t moves (t-th move by the opponent). Corrupted: the same game with only the
  last move replaced by another legal column c' such that the result has no must-block, no immediate win for either side, the
  same set of legal columns, and the game is not over (if several c' qualify, one chosen at random, seed 20261122). Positions with
  no valid c' are dropped (their share is reported). Because the model is causal and the two sequences are identical except for
  the last token, every activation before the last position is identical: patching a component means replacing its output at the
  last position only.
- Splits: discovery = analysis split (5,000 games); confirmation = validation split (5,000 games). At most 4,000 pairs per split.
  Every number in S3 is reported on the confirmation split. Game-bootstrap 95% intervals (1,000 resamples) throughout.
- Threat orientation per pair (from the opponent lines through the block cell): vertical, horizontal, diagonal, or multiple.
- Gap = mean margin(clean) - mean margin(corrupted). A patch's *effect* = (mean margin(clean) - mean margin(clean with the
  component's last-position output taken from the corrupted run)) / gap (noising); its *restoration* = (mean margin(corrupted with the
  component's clean output) - mean margin(corrupted)) / gap (denoising).

S1. Components. Exact noising effect of each of the 48 heads and 6 MLP layers (discovery split).
S2. Neurons and the circuit rule (fixed in advance). The 6,144 neurons (activation SiLU(gate) * up at the last position) are
ranked by attribution patching (gradient of the margin times activation difference, discovery split); the top 300 get exact
single-neuron noising; they are sorted by exact effect (positive only). **Circuit C = the shortest prefix of that order whose joint
noising removes >= 80% of the gap on the discovery split, capped at 200 neurons.** Each neuron's pole = the sign of its mean
clean-minus-corrupted activation difference. If the cap is reached below 80%, the pre-registered reading is "no compact neuron
circuit"; C is then the top 200, and S6/S7 use it as "the most important neurons" (said that way in any write-up).
S3. Faithfulness (confirmation split). Predictions:
- (s-1) Necessity: noising C removes >= 80% of the gap (point estimate; interval lower bound >= 70%).
- (s-2) Specificity: noising random neuron sets matched to C by layer (200 draws) removes <= 20% of the gap at their 95th percentile.
- (s-3) Sufficiency: denoising C (clean values of C patched into the corrupted run) restores >= 50% of the gap.
- (s-4) Behaviour: mean-ablating C (dev-mean activation over all positions) lowers block accuracy on all confirmation must-block
  positions by >= 30 points, while accuracy on the control set (`tactics.control_set`, teacher's best move on non-tactical positions)
  falls by <= 5 points, and layer-matched random sets of the same size lower block accuracy by <= 5 points (median of 50 draws).
- (s-5) Cross-method replication of the tactic atlas: among the 48 heads, L0 H3 is in the top 3 by noising effect; among MLP layers,
  layer 5 has the largest effect.
- (s-6) Orientation: C (fixed above) removes >= 60% of the gap within each of vertical, horizontal and diagonal threats; and a circuit
  built by the same rule within each orientation is smallest for vertical threats. Reported per orientation with intervals.
S4. Mechanism, descriptive (no pass/fail): for each neuron in C, (i) a receptive field: the gradient of its activation with respect
to the residual stream at its input, averaged over clean positions, projected on the board probe's mine/theirs directions for each
of the 42 cells (probes refit as in addendum (k), read point before the neuron's layer); (ii) its direct effect on each column's
logit (output weight through the unembedding); (iii) its mean effect split by block column and orientation. Neurons are grouped by
the column they promote; the write-up states the algorithm these groups imply and checks it against (s-6).
S5. Freeze. `results/block_circuit.json` (C, poles, effects, all S1-S4 numbers) is committed and its hash recorded in docs/LOG.md
before anything in S6 or S7 is computed. Nothing in C changes afterwards.
S6. Test A, the existing descriptions (descriptive: by chance only about |C| x 120 / 12,288 of C's poles are among the (q)/(r) units).
(i) How many of C's poles were described in (q)/(r), their held-out F1 as reported, and their frozen programs' *tactic agreement*:
the best held-out F1 of the program against the ground-truth concepts block_now_c0-c6 and block_now_any (validation split, >= 4
stones). (ii) Reverse: which of the 120 real (q)/(r) units have tactic agreement >= 0.5, and where each ranks in S2. A new analysis
of frozen programs, labelled as a follow-up; no (q)/(r) result is re-scored or edited.
S7. Test B, a blind Neuron Scientist run on the circuit (study (s), workspace `ns3/`, run on a separate Claude account).
- Units: the top 20 poles of C by exact effect (all of C if smaller), 20 decoys, 10 random directions (comparability with (r)),
  shuffled behind opaque ids. Decoy for each circuit pole: a pole of a neuron in the same layer, outside the top 1,000 of the S2
  attribution ranking, nearest on standardised (log dev-p97 magnitude, activation kurtosis), excluding all (q)/(r) units and C.
- Protocol identical to (r): the same prompt, tools, Board API, 8 dev-metric calls, firing beyond dev p97 / p3, >= 4 stones. The
  agent is not told about blocking or that a circuit exists.
- Physical blinding: the agent gets a bundle built by `scripts/38_ns3_bundle.py` with the code, data and the `ns3/` workspace only;
  docs/PLAN.md, docs/LOG.md, results/, ns/, ns2/ and the answer key are not in it, and the bundle's file list is published.
- Measures (validation split, >= 4 stones): tactic agreement (as in S6), held-out F1 against the unit's own firing, and a text-only
  check: a fresh model, blind to group, reads each English description and its effect line and answers "does this describe the
  opponent threatening to win, or blocking it?" (yes / no).
- Predictions. (s-B1, headline) at least half of the circuit poles reach tactic agreement >= 0.5, and at most 10% of the decoys do.
  (s-B2) the text-only check says yes for at least half of the circuit poles and at most 10% of the decoys. (s-B3) the circuit
  poles' median held-out F1 against their own firing is at least 0.10 above the decoys'. (s-B4) random directions: as in (r),
  reported for comparability only.
- Firing threshold. p97 / p3 is kept as the primary definition: it is the tail Goodfire analyse (p97 positive, p3 negative) and the
  one (q) and (r) used. Base rates (analysis split): must-block in a given column 1.6-2.2% of positions, in any column 13.1%. A
  column-specific block detector therefore fits inside a 3% firing rate; a detector of *any* must-block cannot (its top 3% covers at
  most about a quarter of must-block positions). Tactic agreement does not depend on the threshold; held-out F1 against own firing
  is also reported at p90 and p80 as a secondary measure (frozen programs re-scored, no agent re-run).
Reading of the outcomes. (s-1) to (s-4) hold and (s-B1) holds: the describing agent, not told what to look for, recovers the units that
causally implement blocking, the first validated case for the method. (s-1) to (s-4) hold and (s-B1) fails: the circuit is real and the
agent's per-unit descriptions miss it; the post says so, with examples. (s-1) fails: blocking is not carried by a compact set of neurons
in this model, and S7 is reported as a test on the most important neurons.
Not registered here: Test C, an agent that searches for the mechanism itself (chooses which components and neurons to study, with
patching tools) rather than describing given units. That is the step an automated researcher needs beyond the Neuron Scientist; it
gets its own addendum before any run.
Compute: one RTX 4090 pod (Secure, $0.89/h), estimated 2-4 hours; the CUDA guard and the "pull, then terminate" rule apply.

**2026-11-23 (t), after the (s) circuit was frozen and before any (t) computation. Horizontal and diagonal blocking: if not a small
set of neurons, what carries it?**
Why. In (s) the same circuit rule found a compact 53-neuron circuit for vertical threats and none (cap 200) for horizontal or diagonal
threats. A vertical threat lives in one column; horizontal and diagonal threats combine stones across columns. Question: is the
horizontal/diagonal computation spread over many neurons but concentrated in a few *directions* of neuron space, and does attention
carry more of it? This is the project's central question (neurons vs directions as the unit of analysis) asked on one behaviour with an
exact answer key. (s) results, Test A and the Test B units are untouched; nothing here changes C.
Known at registration: the (s) orientation numbers in docs/LOG.md (vertical 53 neurons; horizontal, diagonal: cap; C removes 87 / 71 / 60%)
and the (s) head ranking for all threats (L0 H2 first). No (t) number has been computed.
Design. Model, pair construction, metric, splits and bootstrap as in (s) S0, but all valid pairs are built (no 4,000 cap at construction)
and then split by orientation (vertical, horizontal, diagonal; "multiple" excluded), at most 4,000 pairs per orientation per split.
Everything is fitted or chosen on the discovery split and reported on the confirmation split.
- Scope: **layers 0-4 only**. Anything in layer 5 reaches the move through a 7-column readout, so any method gets a trivial
  low-dimensional answer there; restricting both methods to layers 0-4 makes them explain the computation upstream of that bottleneck.
  The all-layer version is reported as secondary.
- Ceiling E_all(o) = noising effect of all 5,120 neurons of layers 0-4 at the last position, per orientation o. Target = 0.8 x E_all(o)
  (both neuron sets and subspaces of layers 0-4 are bounded by it).
- T1, neurons. The (s) rule restricted to layers 0-4: attribution ranking, exact single-neuron noising of the top 1,000, sorted by exact
  effect, joint-noising curve at k = 1..100, then every 10 to 1,000, then the attribution order in steps of 100 to 5,120.
  N80(o) = smallest k reaching the target (discovery), confirmed on the confirmation split.
- T2, directions. Per layer l in 0-4, the SVD of the discovery matrix of clean-minus-corrupted activation differences at the last
  position (pairs x 1,024); its top-k right singular vectors U_l. Subspace patching replaces the component of the activation in span(U_l)
  by the corrupted run's: a' = a + (a_corr - a) U_l U_l^T. The same k in each layer, k in {1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64};
  D80(o) = 5k for the smallest k reaching the target (discovery), confirmed on the confirmation split.
- Controls: random subspaces (Haar, same k per layer, 50 draws) at k(D80); and T2 for vertical threats with the same procedure.
- T3, heads: last-position noising of each of the 48 heads per orientation; the joint top-m curve (m = 1..10).
Predictions (confirmation split; all per orientation).
- (t-1) N80(horizontal) and N80(diagonal) are each >= 3 x N80(vertical).
- (t-2) D80 <= 30 directions for each of the three orientations, and the D80 subspace removes >= 0.75 x E_all(o) on the confirmation split.
- (t-3) The ratio N80 / D80 is larger for horizontal and for diagonal than for vertical.
- (t-4) Random subspaces of the same size remove <= 10% of the gap (95th percentile of the 50 draws).
- (t-5) The largest single-head noising effect is larger for horizontal and for diagonal threats than for vertical threats.
Reading. (t-1) to (t-4) hold: vertical blocking is carried by a few neurons, horizontal and diagonal blocking by a few directions that are
spread across many neurons; the post says the right unit of analysis depends on the computation. (t-2) fails for horizontal/diagonal:
those computations are high-dimensional in neuron space (neither basis is compact), said as such. (t-1) fails: the neuron counts are
comparable and the (s) difference came from the 200 cap and the 80% target. Descriptive: which layers the D80 directions sit in, their
receptive fields on the board probe (as in (s) S4), and how many neurons each direction loads on (participation ratio).
Compute: one RTX 4090 pod, estimated under 1 hour; CUDA check; pull, then terminate.

**2026-11-23 (u), before any (u) computation. The vertical blocker, end to end, and what its demo may claim.**
Scope: vertical must-block pairs only (S0 of (s); clean = the opponent's last move made three in a column with the cell above empty;
corrupted = that move played elsewhere). The vertical circuit V is recomputed with the (s) rule on the (s) discovery pairs (expected 53
neurons; any difference is reported). Readout neurons R = the members of V in layer 5. Directions = the (t) top-3 singular directions of
clean-minus-corrupted differences in each of layers 0-4 (15 in all), refitted on the same discovery pairs. Confirmation split for every
number. Run on a GPU host (`scripts/40_vertical_map.py`).
Predictions.
- (u-1) Attention: at the last position, L0 H2 puts >= 50% of its attention on earlier moves in the same column as the last move (mean
  over clean confirmation pairs), against the share expected if it attended uniformly over earlier moves (reported).
- (u-2) Feeding the readout: patching the 15 directions (layers 0-4, last position, corrupted values) moves R's activations by >= 70% of
  their clean-minus-corrupted difference (effect-weighted mean over R).
- (u-3) Column alarms: >= 80% of R have their largest effect on one block column and promote that column (direct-logit argmax).
- (u-4) Meaning: the first direction of a layer tracks the opponent's run on top of the last-move column (number of consecutive opponent
  stones from the top, counted with the cell above empty, else 0): |Spearman| >= 0.5 over all confirmation positions with >= 4 stones,
  in at least 3 of the 5 layers.
- (u-5) Demo switches (mean-ablation at every position, so they work in live play; confirmation split, must-block positions with >= 4
  stones by orientation, plus the (s) control set): (i) L0 H2: vertical block accuracy falls >= 20 points more than control accuracy;
  (ii) the 15 directions (projection set to its dev mean): vertical falls >= 30 points, control <= 10 points, random 3-per-layer
  subspaces <= 5 points (median of 20); (iii) R: vertical falls >= 30 points, control <= 5, random layer-5 sets of the same size <= 5
  (median of 20). Horizontal and diagonal accuracy under each switch is reported.
What the demo may claim: only numbers computed here or in (s)/(t), each shown next to its switch; if a (u-5) prediction fails, the demo
shows the measured effect and says it is smaller than predicted. The browser model must match PyTorch under every switch (max logit
difference <= 5e-3 on the exported reference games), checked by `tests/check_web_port.js`.
