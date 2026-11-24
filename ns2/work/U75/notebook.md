# U75 notebook (layer 4, pole +, threshold 0.877, dev max 11.77)

## Observations (examples, bands 0-9)
- Top bands: early/mid game; column 2 height is 0 or 2 (odd heights rare); (2,2) empty; (1,2) rarely X; (0,1) often X; col3 height 1 almost never.
- No firing positions have an immediate win for me.

## Minimal pairs (act)
- 4,4,1,1 = 4.9; 4,4,3,3 = -0.55; 3,3,1,1 = -0.75; 4,1,1,4 = 0.09 (colours matter).
- 0,2,6,2 (O,O in col2) = 1.2; same in cols 1,3,4,5 ~0. col2 triple O 4.1; X on top of col2 kills.
- 94550 (1,6,2,6,5,3,3,6,6,2) = 11.2; its last move O->(1,2) jumps from -0.3. Replacing X(1,3) with X(0,4) -> 1.2; O(0,3)->(0,4) -> -0.2.
- 4,4,1,1 + col3 stones: [O,X] 4.2, [X,X] 1.9, [O,O] 1.1, [X,O] -0.4. + col2 [X,O] -> 6.9.
- Pattern: col2 empty or capped by O at row1; col3 empty or X at row1 (checkerboard X(0,2)O(1,2)/O(0,3)X(1,3) best).

## Hypotheses
H1: col2 height 0 or 2 with O at (1,2). score 1: F1 0.120 (P .067 R .554) -> far too broad.
H2: (2,2) empty, (1,2)!=X, (1,3)!=O, (0,1)==X. score 2: F1 0.129.
H3: H1 + col3 condition (empty, or X at (1,3)); h3 != 1.
score 3 (H3): F1 0.150 (P .093 R .387). Misses include col2 [O,X] firing at 3.6 (pos 6119, O vertical three in col 3); FPs many with block ok but act ~0.

## More minimal pairs
- 4,4,1,1 + col2 [O,X] -0.57, [X,X] 0.11, [O,O] 2.7, [X,O] 4.2/6.9. col3 [X,O] kills.
- Checkerboard 2x2 block (me (0,2),(1,3); them (0,3),(1,2)) fires robustly at even ply (2,3,X,2,3,2 family 3-5).
- Parity: same display pattern with me = second player (3,2,2,3,6) does NOT fire (0.1); 6,6,2,3,3,2 fires 5.8. But dev odd-ply fires exist (~30% of top band) on fuller boards.
- X at (0,4) in the 94550 frame or 13840 kills firing; other stones modulate strongly and nonlinearly.
- Extending cols 2/3 to height 4 mostly kills.

score 4 (points rule, ply, no win): F1 0.183.
score 5 (block score + me_first + no immediate win): F1 0.202 (P .184 R .224), sim share 0.03.
score 6 (+ ply <= 18): F1 0.214 (P .215 R .213), AUROC .594, sim share 0.03. Best.

## Steer
Zeroing 94550: col2 -6, col3 +5 pts; 2,3,1,2,3,2: col6 -3; 4,4,1,1: col3 +5, col4 -5; others ~0. Max on 4,4,3,3: col5 +9 col2 -9; on 0,4,6,4: col3 +12. Weak, inconsistent.

## Synthesis
2,6,1,6,5,3,3,6,6,2,0,0,4,4 = 12.58 (beats dev max 11.77); 2,6,1,6,5,3,3,6,6,2,4,4,0,0 = 12.40; 1,6,2,6,5,3,3,6,6,2,0,0,4,4 = 12.47.
Built by row-0 mine stones capped by theirs on row 1, with the col2/col3 checkerboard.

## Conclusion
Confidence low: best F1 0.21. Real local regularity (cols 2-3 low block) but strong nonlinear dependence on rest of board; looks like a mixture/distributed direction.
