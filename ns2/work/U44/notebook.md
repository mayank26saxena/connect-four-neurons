# U44 notebook (layer 2, pole +, thr 0.877, dev max 2.397)

## Observations
- Top examples: often the opponent's last stone is stacked (row>=1), frequently on top of another opponent stone
  (vertical OO ending with the last move), often in columns 1, 4, 5. Many exceptions (e.g. 80700 last move at row 0).
- Steer (4 positions, max and zero): changes <= 0.02 in any column. No measurable effect.
- Minimal pairs: c,c,a,c (X,O,O stack, last move on top): col1 ~1.36, col5 ~1.24, col0 ~0.76-0.95, col4 0.26-0.81,
  col2 ~0.4-0.6, col3 0.0-0.5, col6 -0.7. Same stack O,X,O is weaker (3,1,1,1 0.72; 3,5,5,5 0.45).
- Last-move column alone (3,3,p,1 / 3,1,p,1) does not drive it; depends a lot on context. Looks distributed.

## Hypotheses
H1: opponent just stacked onto their own stone (vertical pair of theirs ending with last move), in col 0,1,4,5.
H2: weighted mix of cell occupancy (O at (2,1)/(2,5)/(2,4)).

## Score 1 (p1, H1): F1 0.060, P 0.035, R 0.211, AUROC 0.518, sim share 0.03. No signal; H1 dropped.

## More probes
- Within a game the activation alternates sign by ply (perspective flip), e.g. one game high on all odd plies,
  another high on all even plies; base level is game-wide, not driven by the last move alone.
- Not the engine eval (band 0 positions include winning ones, band 9 include slightly losing ones).
- Single-feature histograms (bands 0-2 vs 6-9, 300 examples/band, files deleted after): high band over-represents
  ply 5-14, last move landing on row 2, last col 1/4/5, X at (1,4), O at (2,4), X at (0,5). Differences modest.
- Minimal pairs: a,4,4,4 (O over X over O in col 4, last move on top) fires for a=1,3,5,6; 5,4,4,x without O at (2,4)
  is low. Effect fades after further moves.

## Score 2 (p2: col4 O-over-X or last move row 2 in col 0/1/4/5): F1 0.079, AUROC 0.567, sim 0.04.
## Score 3 (p3: col4 O-over-X only): F1 0.086, P 0.065, R 0.128, AUROC 0.536, sim 0.05.
   FPs/misses show no shared pattern.
## Score 4 (p4: ply 5-14, last move row 2-3, col 1/3/4/5): F1 0.119, P 0.079, R 0.242, AUROC 0.579, sim 0.05. Best.

## Steer: 4 positions, max and zero: every column changes by <= 0.02. No measurable effect.
## Synthesis: best 1,4,6,4,1,5,1,1,2 = 2.198 (dev max 2.397, below).
## Conclusion: no clean concept found. Weak tendencies only. Could be a random direction or a very distributed
   feature. Confidence low. Stopped at 4 of 8 score calls because the rest would just be fitting noise.
