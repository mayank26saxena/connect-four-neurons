# U26 notebook (layer 3, pole -, threshold 1.131, dev max 2.864, firing 3%)

## Observations
- Examples (40 + band 8/9 extra): firing positions are early-ish (ply 4-20), last move more often col 2/3.
- Per-cell histograms by band: weak differences only (O at (0,2) 51% vs 42%; (0,4) empty more often in firing).
- Activation alternates strongly by ply within a game (e.g. 1,5,4,0,2,3,3,1,x: ply 8 -0.65, ply 9 fires for almost any last move x).
  So it depends on the whole configuration seen from the mover's side, not on the last move much.
- 4-stone grid X0,Oa,X3,Ob: fires only for O at {2,6} (1.86) and {6,3} (1.63). Mirror image 6,4,3,0 gives -1.43 -> not mirror symmetric.
- Steering (zero) on 8 top positions: changes <= 0.04 in any column; effect ~none.
- Teacher scores in firing positions often mildly negative for me, but not consistently.

## Hypotheses
H1: early game + last move col 2/3 (base-rate proxy).
H2: opponent stones in bottom-center (0,2) with (0,4) empty.
H3: no clean concept / random direction.

## Score calls
1. p1 (ply<=16 and last move col 2/3): F1 0.094 (P 0.055, R 0.311), AUROC 0.575, sim -0.04.
2. p2 (top stone of col 2 is theirs at height 1 or 3, ply<=20): F1 0.110 (P 0.071, R 0.245), AUROC 0.574, sim -0.02. Best.
3. p3 (hand-weighted sum of histogram-enriched single features: col2 top O odd height, O low in col 6, cols 0/1/6 low, col 4 empty, early game): F1 0.102, AUROC 0.541, sim -0.06.
Stopped scoring: three genuinely different ideas all near chance; FPs and misses show no shared pattern.

## Further minimal pairs
- Extending 1,3,0,4,5,2 with (X,O): O playing column 6, X having a stone in col 6, or O dropping directly onto X's last stone gave higher values; O making col-2 height 2 was consistently low. None of these generalised (single-feature histograms: last-two-same-column 0.25 vs 0.26; col-6 occupancy no difference).
- Activation swings by >2 between consecutive plies of the same game, often regardless of where the last stone goes -> depends on perspective (whose stones are whose) across the whole board.

## Steering
8 positions zeroed + 3 forced to max: every column changes by <= 0.04. Effect: none measurable.

## Synthesis
Best found: dev top game 3,2,1,6,1,3,3,6,3,6,6,3,1,1 (2.864 = dev max; tie). Others 2.684, 2.645, 2.605, 2.354 (below).

## Conclusion
No clean concept; looks like a distributed/mixed or random direction. Confidence low.
