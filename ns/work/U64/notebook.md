# U64 notebook (layer 3, pole +, threshold 2.020, dev max 3.422, firing rate 3.0%)

## Examples
- 40 examples across bands + 3 extra seeds of band 5 (30 samples): every firing position (bands 5-9) is the EMPTY board (ply 0), all at exactly 3.422 (dev max).
- Band 4 (1.2-2.0) are ordinary mid-game positions, no visible common pattern; none crosses threshold.
- Firing rate 3.0% ~= 1 / mean game length, consistent with "one firing position per game = the start".

## Hypotheses
H1: fires iff board is empty (ply == 0). Start-of-sequence detector.
H2 (alt): fires on very early positions generally. Rejected by act: after 1 move (cols 0,3,6) act is -0.1 to -0.2; after 3,3 -0.12.

## Tests (act)
- empty -> 3.422; [3] -> -0.175; [0] -> -0.215; [6] -> -0.100; [3,3] -> -0.116. Sharp drop after any stone.

## score 1 (p1.py: fires = ply==0, level 9/0)
F1 0.985 (P 1.000, R 0.971), AUROC 0.986. Simulation share 0.01 (recovers 1.1% of ablation damage; ceiling 85.1%).
Misses (59) are mid-game positions just above threshold (2.0-2.4), e.g. 4,0,2,2,3 and 4,0,3,6,3,4,2 (opponent has open three on the bottom row, two must-blocks, lost position), 1,4,4,1, 6,5,3,3,5 (nothing special).

## Mid-game exploration (act)
- Single-stone variations of short games change activation a lot (-0.6 to 2.3) with no clear rule.
- Opponent double must-block positions: 3,0,4,0,2 1.44; 3,3,4,4,2 1.97; 3,6,4,6,2 1.00; 2,6,3,6,4 0.91. Elevated but not reliably firing.

## score 2 (p2.py: same fires; level adds 5 for opponent double threat, 3 single, 2 otherwise)
F1 0.985, simulation share 0.01. No gain, so I dropped it and kept p1.

## steer
- empty board, zero: no change at all (center 0.44 unchanged).
- 4,0,2,2,3, 1,4,4,1, 6,5,3,3,5, 3,2,6,3,1 to max/zero: all changes <= 0.02. No measurable effect on the move.

## synth
- empty board = 3.422 = dev max (ties, does not beat it). Mid-game best 2.295 (4,0,2,2,3).

## Conclusion
U64 is a start-of-game detector: it fires on the empty board (ply 0). The low simulation share is because the unit's ablation effect comes from small graded mid-game activations that I could not describe simply.
