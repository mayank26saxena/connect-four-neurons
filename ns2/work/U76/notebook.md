# U76 notebook (layer 3, pole +, threshold 0.811, dev max 8.325)

## Examples (band 0-9, 40 + 12 top)
- Top band: column 2 is often empty/low while col 1/col 3 are tall. Many top examples have col 1 reading (bottom-up) O,X,X,(O) from mover's view.
- Activation strongly depends on side-to-move (mover frame): in a game it fires on alternate plies only.

## Hypotheses
H1: my stones at (1,1) and (2,1) (col 1 rows 1-2), col 2 empty/low. (column-1 specific; mirror col 5 does not fire)
H2: tall column next to empty column 2 (colour-agnostic) -- refuted: 3,3,3,3,1,1,1,1 = -0.03.
H3: floating empty cells next to my stones -- refuted by same test.

## act tests
- 6,1,1,5,1,1 (col1 O,X,X,O, me P1) 1.23 FIRES; same pattern in col 0/2/3/5/4: all < 0.2.
- adding O at (0,2) under it -> -1.9; filling col 2 kills it (0.1).
- col1 O,O,X: 1.03 fires; O,X,O: -0.28; O,X,X uncapped with O(0,5): -1.79 (but 1.04 in another context).
- parity: same stones, other side to move -> ~0.

## Scores
- s1 (X at (2,1), O at (0,1), col2 h<=1): F1 0.121, P .128 R .116, AUROC .545, sim -0.12. FPs look identical to the pattern -> context matters.
- per-cell histograms by band (band 9 vs band 1): X at (4,3) 96% vs 25%; O(2,3) 73 vs 35; X(2,1) 73 vs 21; O(3,4) 70 vs 18; col 2 low, col 3 tall (5.7), col4 4.6.
- s2 (X at (4,3)): F1 .177 P .10 R .74 AUROC .767 sim -0.11
- s3 (col2<=1 and (X(4,3) or X(2,1))): F1 .178 P .116 R .376 sim -0.03
- s4 (X(4,3) and col2 h<=2): F1 .249 P .172 R .45 AUROC .69 sim 0.03
- act: filling column 2 up to row 2/3 kills firing (3.09 -> 0.54 -> 0.29). X(2,1)+X(4,3) superadditive (1.2 + 1.3 -> 3.1).
H5: the unit is about the empty, not-yet-playable cell (3,2) and its neighbourhood: my stones on its rising diagonal (2,1),(4,3), their stones on (2,3),(3,1),(3,3),(3,4).
- s5 (weighted neighbourhood of (3,2), threshold 5): F1 .204 P .142 R .365 sim -0.01 (worse; weights hurt)
- band hist: top bands have cols 3,4 nearly full (mean 5.7, 4.6), col 2 low; last move often col 4 or col 1.
- s6 (X(4,3), col2<=2, col4>=4): F1 .245 P .196 R .326 AUROC .64 sim 0.05
- s7 (s4 OR col-1 stack O,X,X with col2<=1): F1 .242 P .162 R .478 AUROC .70 sim -0.01
Best: s4 (F1 0.249). Precision never above 0.2: many boards with the pattern do not fire, and many firing positions (band 5-6, often early sparse boards) share no pattern I could find. Looks like a mixture.

## Steer
Effects small and not consistent across positions (max ~0.1 probability shift): +col3 in one, +col1/-col2 in another, -col4 in another, +col5 when ablated in synthesis. Call it 'no consistent effect'.

## Synthesis
3,1,3,3,4,3,3,5,4,4,1,4,4,0,1,1 -> 9.93 (beats 8.33): col1 O,X,X,O; col2 empty; cols 3/4 X,X,O,O,X; me at (4,3),(4,4).
3,1,3,3,4,3,3,3,4,4,1,4,4,5,1,1,6,0 -> 9.74; ...,6,0 variant 9.69.
