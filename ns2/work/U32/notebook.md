# U32 notebook (layer 0, pole -, threshold 0.001, dev max 0.005; activations tiny)

## Examples
Top bands: last move (opponent's) almost always in column 1 or 5 (sometimes 0/4). Player to move tends to have many stones in col 0 and col 4.

## Hypotheses
H1: fires when last move is col 1 or col 5 AND the player to move has a large share of their stones in cols 0 and 4.
H2: pure last-move-column lookup (1/5) -- too broad (3,3,3,1 = 0.000).
H3: position-agnostic token mixing (layer 0): weighted share of my moves per column.

## act tests (a,3,a,L grid)
- L in {1,5} required: other L give ~0.
- my stones col 0 / 4 -> 0.003-0.004; col 2 -> 0.001; col 1,3,6 -> 0; col 5 -> negative (5,3,5,3,5,3,5,1 = -0.005).
- opponent stones' columns matter little (opp in col 5 slightly lowers).
- order of my moves doesn't matter much (0,0,6,6 vs 6,6,0,0 both 0).

## score 1 (p1: last in {1,5} & my weighted share(0,4) >= 0.4): F1 0.237, P 0.26, R 0.22, AUROC 0.60
Band histograms of last_col: band 9 = only 1/5 (+ few 3/4); bands 5-7 mixed (1 most common, 3/4 frequent).
act grid a,L,a,L,a,L: only L in {1,5} with my stones in 0/4 gives >=0.002; other L ~0-0.001 (noise level).
Opponent stones in cols 0, 4, 5 lower it (0.001 vs 0.002).

## score 2 (p2: added opponent penalty): F1 0.200, P 0.30, R 0.15. Worse recall.
First-move histogram: band 9 has first move 0 in ~50% (base ~12%), but act shows first token alone doesn't matter (consistent with owner share of col 0).
Rule holds for both parities (odd-ply tests with my stones in 0/4 and last 1/5 fire 0.002).
Firing at threshold is noisy: bands 5-7 have last col 1/5 only ~45%. Trying additive token model (p3).

## score 3 (p3: additive token model, guessed weights): F1 0.240, P 0.23, R 0.25, AUROC 0.61
Cleaner 12-ply act probes (my 6 stones all in col c, opp in 2/3, last L):
- my col: 0 -> 0.004, 4 -> 0.002, 1/2/3/6 -> 0.000, 5 -> -0.004 (L=1/5)
- opp col (my=0): 1,2,3 -> .003; 4,6 -> .002; 5 -> .001
- last col with my=0: 1,5 -> .004; 2,3,4 -> .001; 6 -> .002; 0 (my=4) -> 0
Looks like gate(last col) x (my share in col0*4 + col4*2 - col5*4 + opp penalties). Recency/order irrelevant. Max .005 reached by 4,2,4,2,0,2,0,3,0,3,4,1.

## score 4 (p4: gated model, thr 1.4): F1 0.111, P 0.39, R 0.065 (program fires 0.5%). Threshold too strict; try 0.7.

## score 5 (p5: p4 with thr 0.7): F1 0.199, P 0.22, R 0.18. Probe-fitted weights do not transfer to dev; near-threshold firing is noisy.
Stopping scoring. Best = p3 (F1 0.240, AUROC 0.61). Simulation reported nan (unit has no measurable effect).
## steer (to max) on 3 positions: change 0.00 in every column. No effect.
## synthesis: 0,2,0,2,0,3,4,1,4,3,4,0,0,4,0,1,4,5 -> 0.006 (beats 0.005); variants ending 5,4,1 / 6,4,1 also 0.006; 0,2,0,2,0,3,4,3,4,3,4,0,0,2,0,1 -> 0.005 beats.
Conclusion: low confidence. Clear top-end pattern (last move col 1/5 + mover's stones in cols 0/4, none in col 5), but it explains only ~25% of threshold firing.
