# U49 notebook (layer 5, pole -, threshold 0.459, dev max 3.726)

## Observations
- Top examples (band 9) look heterogeneous: early games, opponent stacks/twos, X stones on edges. No single shape obvious.
- 4-ply grid X=a,a / O=b,b: almost everything ~0 except (X6,O1)=2.19, (X2,O5)=0.88, (X0,O5)=0.55, (X2,O6)=0.48; not mirror-symmetric. Lookup-like.
- Activation is spiky along a game: fires after one move, drops to ~0 after the next (e.g. 4,4,1,0,3,2,2,3: 2.36 -> -0.2 -> 2.12).
- Last-move placement matters strongly (3,6,4,6,4,2,2,3,3,2,x: x=3 3.62, 5 1.41, 6 1.31, 1 -0.02).
- Single-feature histograms by band: firing skews to early game (ply<=20), all 7 columns open, last move in col 3 (34% in top band vs ~14%), slightly more threat-creating moves for both sides. Weak.
- teacher scores: no consistent value story (depth-8 scores noisy).
- steer max: small, raises col 2 by +0.06..+0.15 in several positions, lowers col 3 sometimes; steer zero on top positions changes <0.05.

## Hypotheses
H1: early game + last move centre column (weak baseline).
H2: opponent has several moves that create a new threat cell (initiative) - weak in histograms.
H3: no clean concept / mixture or random direction.

## Score calls
- s1 (p1.py, H1 early game + all columns open + last move col 3): F1 0.071 (P 0.046, R 0.156), AUROC 0.528, sim share 0.01. Chance level.
- s2 (p2.py, H2 early game + count of threat-creating moves for both sides, minus immediate tactics): F1 0.075, AUROC 0.528, sim share 0.01. Chance level.

## Further minimal pairs
- 4,4,1,0,3,2,2,x: only x=3 fires (2.36); every other last move ~0. 6,2,6,2,6,6,4,4,2,4,x: x=4 2.86, x=5 1.08, others ~0.
- O two stacked at bottom of col 1 + X stones in cols 4-6 fires (6,1,6,1 2.19; 6,1,4,1 2.29; 4,1,6,1 2.17) but 5,1,5,1 / 3,1,3,1 / 0,1,6,1 do not. Only col1/col5 work for the O stack.
- Move ORDER matters for the same final board: 3,6,4,6,4,2,2,3,3,2,3 = 3.62 vs 4,6,4,6,3,2,2,3,3,2,3 = 3.92 vs 3,6,4,6,2,2,4,3,3,2,3 = 0.64 (different board though). Same board, different order: 3.62 vs 3.92.
- Last-move-relative histograms (blocked my win, new their wins, neighbours, cell above a threat) show no band differences.

## Steer
- max: takes 3-15 points from col 3 in several positions and moves it to col 2 or col 6 (3,3,4,2: col2 +0.15, col3 -0.15; 6,1,6,1: col3 -0.03 col6 +0.03; 4,4,1,0,3,2,2,3: col3 -0.04 col6 +0.04; 0,3,5,3,0,6,5,5: col3 -0.07). zero on top positions: changes <0.05.

## Synthesis
- 4,6,4,6,3,2,2,3,3,2,3 = 3.915 BEATS dev max 3.726. 4,6,3,6,4,2,2,3,3,2,3 = 3.70, 3,6,4,6,4,2,2,3,3,2,3 = 3.62, 4,6,4,6,3,2,2,3,3,2,3,0,0 = 3.53.

## Conclusion
No board pattern found; firing is sparse, lookup-like, sensitive to exact last move and even move order. Weak skew to early game and last move in col 3. Confidence low (possible random direction / mixture). Stopped after 2 score calls since further programs would be guesses.
