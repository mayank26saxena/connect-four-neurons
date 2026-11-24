# U62 notebook (layer 0, pole -; threshold 0.285; dev max 1.653)

## Observations (examples, 40 + ~135 band 5-7 samples)
- Top of distribution is ply-1 positions: opening in col 5 -> 1.653 (dev max), col 4 -> 0.972, col 6 -> 0.285 (exactly threshold, not firing), cols 0-3 negative.
- Band 5-7 samples: ~85% have odd ply (opponent moved first, I am second player) and last move in col 4 or 5 (col 5 > col 4); a few col 1/3/6 and even-ply.
- Random-game act sweep: odd ply + last col 4/5 fires ~40-70% when ply < 6, rarely later (dilution in layer-0 attention?). Dev engine games fire later more often.

## Minimal pairs (3-ply games x,y,5)
- My (second player) earlier stone in col 1 strongly suppresses (x,1,5 ~ -0.2..-0.5); col 4 also lowers.
- Their earlier stone in col 0 suppresses; in cols 1,3,4,5 raises (x,2,5: 0:-0.09, 1:0.50, 3:0.66, 4:0.59, 5:0.56, 6:0.21).
- Looks like a layer-0 token mixture: last-token value (col5 > col4) plus additive contributions of earlier moves by column and player.

## Hypotheses
H1: fires iff opponent is first player (odd ply) and last move was col 4 or 5.
H2: H1 restricted to early game / plus suppression by my stones in col 1.
H3: (fallback) mixture of last-move token with history; no clean board concept.

## Score calls
1-2. p1 (H1: odd ply & last col in {4,5}). Accidentally ran twice (call 1 output truncated). F1 0.225 (P 0.137, R 0.636), AUROC 0.757, sim share 0.05. Recall OK, precision bad: history decides.
3. p2: hand-set additive history model from minimal pairs: base[last col] + mean over earlier stones of per-(player,column) weights; odd ply only; ply-1 table. F1 0.433 (P 0.35, R 0.57), AUROC 0.768.
4. p3: re-tuned weights (my col 0 more negative, my col 2 positive, lower bases for cols 0-3,6). F1 0.446, AUROC 0.783.
5. p4: integer level cuts instead of linear; sim unchanged 0.05 (unit has no measurable steering effect at firing positions; zero-ablation damage presumably from the negative side, which I do not model).
6. p5: fires threshold on my score raised to 0.42: F1 0.482.
7. p6: threshold 0.55: F1 0.511 (P 0.525, R 0.498), AUROC 0.742. Stopping (1 call left).

## Minimal pair notes
- Weights roughly uniform over history position (not recency-weighted), contributions diluted as 1/ply; gating by last token (odd ply, col 5 > 4 >> 3,6 > others). Even ply never fires in tests (3,2,4,c all ~0).
- Interactions exist (gated MLP: product of two linear terms), e.g. 1,0,5,3,3 = 0.018 while additive model predicts firing.

## Steering
- 4 positions (5; 3,2,5; 6,0,3,4,0,0,4,3,4,1,1,5,1; 4,4,3,2,4,2,5; plus a negative one), to max and zero: all changes <= 0.01. No measurable effect.

## Synthesis
- Ply-1 opening in col 5 = dev max 1.653 (equal, not beaten). Best multi-move: 5,2,4,2,3,6,5 = 0.933. Could not beat 1.653.

## Conclusion
Layer-0 token-mixture unit. Gate: the opponent is the first player and just played col 5 (or 4). Magnitude: their earlier stones in cols 3-5 help, their col-0 stones hurt; my (second player's) stones in col 1, 0, 4 hurt, col 2/5 help. Medium-low confidence: F1 0.51, clear interactions.
