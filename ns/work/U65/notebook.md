# U65 notebook (layer 4, pole +, threshold 0.807, dev max 8.687, rate 3%)

## Observations (examples, ~70 boards across bands)
- Top bands dominated by early openings (ply 2-12) and by boards with column 1 empty (band 9: 26/30 col1 empty vs ~30% in bands 0-3).
- Openings: after 2 plies, fires iff opponent's first stone is on the bottom of col 3 and mine is not col 3 (2,3 / 0,3 / 4,3 / 6,3 fire; 3,x and 3,3 do not).
- 4-ply grid X:0,0 + O:a,b -> O stones on cols 3-5 give 3.6-7.9; O on col 1 kills it. With X on col 6 the grid is not mirror-symmetric (needs O on col 3 or 2/3).
- Strong alternation: after my (to-move player's) own opponent's move activation high, after the other side's move it is low/negative (sign depends on board from mover's view).
- Steer to max/zero: no measurable change in move probabilities (<=0.09) on 5 positions.

## Hypotheses
H1: column 1 empty + opponent stones in bottom-centre (cols 2-5) -> fires.
H2: opponent owns bottom-centre (0,3) / has more bottom-row centre stones than me.
H3: mixture/random direction; no clean concept.

## Tests
- 1743 prefix (ply 9) + O's 10th move in each column: col 5 -> 8.2, col 2 -> 4.6, col 4 -> 1.8, col 6 -> 0.9, cols 0,1,3 -> ~0.
- 0,3,0,5 (7.9) + pairs: 1,1 -> 3.1; 6,6 -> 1.3; 2,2 -> 1.8; 4,4 -> 0.65; 6,1 (O on (0,1)) -> 0.29; 1,6 (X on (0,1)) -> 2.9.

## More probes
- 2-ply table (X col x, O col y): fires mainly when O is on (0,3) and X is not on col 3/5; stacking O on X is strongly negative (-2..-3.4).
- 3-ply (O stacked twice in col a, me elsewhere): col 6 stack -> 1.5-4.2, col 5 -> ~1; cols 0-4 mostly < 0.8.
- 4-ply O stack in col c with my two stones elsewhere: col 3 with X at 0,0 -> 3.6 / X at 6,6 -> 5.3; col 5 with X 0,0 -> 4.7; my stones in cols 2-4 kill it.
- MIRROR TEST: 1743 game (8.2) mirrored -> 0.07; 4,4,3,2,6,5,4,5,3,3,4 (5.9) mirrored -> -0.05. Strongly left/right asymmetric; likes empty left columns (0-1) and opponent stones low on centre/right.
- Adding any pair of stones to the top positions usually lowers it; it is largest on sparse boards.

## Dev metric
- call 1 (p1, col1 empty + opp>=mine on bottom row cols 2-5): F1 0.177 P 0.107 R 0.508 AUROC 0.686, sim share 0.08. (call 2 was an accidental duplicate run of p1.)
- call 3 (p2, ply 2-14, col1 empty, col0<=2, opp>=mine low stones cols 2-6): F1 0.205 P 0.129 R 0.495 AUROC 0.694, sim 0.08.  BEST
- call 4 (p3, me_first + col1 empty + opp low stone cols 3-5): F1 0.190, AUROC 0.63.
- call 5 (p4, opponent vertical run>=2 on top of a column 2-6 + col1<=1, or opening rule): F1 0.154. Vertical-run idea (from must-block boards with O stacks) does not generalise.
- call 6 (p5, hand-weighted cell score from probes): F1 0.184, AUROC 0.695.
Conclusion: no rule above F1 0.21. Unit behaves like a mixture / possibly random direction: strong spatial asymmetry, sparse-board bias, and no steering effect.

## Steering
- 1743, 0,3,0,5, 6,3, 2,3, 6,2,6, 4,4,3,2,6,5,4,5,3,3,4, 0,5,0,4,4,5: max or zero changes move probs by <= 0.09 (largest: zeroing at 0,5,0,4,4,5 moves ~8 pts from col 0 to col 3). Essentially none.

## Synthesis
- Exhaustive 4-ply search (act): best 0,3,0,5 = 7.9. Beam search (2-ply extensions) from top seeds + 1743 game:
  3,0,4,2,6,5,4,4,3,5,0,2,3,3 = 8.944 (BEATS dev max 8.687). Others 8.2-8.3.

## Final
Submit p2 (best F1 0.205), confidence low: looks like a mixture / possibly a random direction.
