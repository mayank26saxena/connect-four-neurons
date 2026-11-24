# U31 notebook (layer 5, pole +, threshold 0.789, dev max 10.02)

## Observations (examples ex1, b9, b8, b567)
- Top band (3.4-10): mostly opponent has 3-in-a-window on the BOTTOM row -> a single must-block at row 0
  (e.g. 6,3,6,2,4,6,3,1 = 5.0; 3,4,0,3,3,3,1 = 5.5). Some late-game boards with 1-2 legal columns in cols 0-2.
- Two must-blocks (opponent already won, e.g. 2,2,3,3,1) -> hugely NEGATIVE (-100). My immediate win present -> never fires.
- Ply-4 bottom-row patterns: X{2,3}+O{5,6} = 4.4 (fires), X{2,3}+O{0,6} = 0, X{2,3}+O{4,5} = 0, mirror X{3,4}+O{0,1} = -2. Asymmetric, puzzling.
- Mid band (0.8-1.6): many have an opponent threat cell directly ABOVE a landing cell (poisoned column), no must-block.

## Hypotheses
H1: fires when the opponent has a threat I must respect: a single must-block (esp. row 0) or an opponent threat cell
    directly above a landing cell; never when I have an immediate win or the opponent has 2+ must-blocks.
H2: bottom-row horizontal tension (pairs/threes in row 0 with gaps) - early game component.
H3: late-game forced move in left columns.

## Minimal pairs
- 134047 (threat (1,2) above landing): 0.935; replace last O move 4->5 (no threat): 0.495; 4->6: 0.19. Supports H1 weakly.
- After I fill under the threat (opponent now has win for side-to-move): -0.1.

## Score log
- s1 (p1: any single must-block or opp threat above a landing cell): F1 0.081 (P 0.043, R 0.64), AUROC 0.61, sim share 0.19. Far too broad (43% of positions).
- s2 (p2: exactly one must-block, on row 0, not col 3, no own win): F1 0.132 (P 0.256, R 0.089), AUROC 0.54, sim -0.87.
- s3 (p3: anti-centre proxies: centre full / centre poisoned / non-centre must-block): F1 0.071, fires on 46%. Centre-full is not it.
- s4 (p4: p2 + poisoned columns graded): F1 0.082, sim share 0.22. Threat-above precision ~ base rate.
- s5 (p5: p2 + centre full & <=3 legal cols): F1 0.103, sim -0.81.
- s6 (p6: fires=p2, level=p4 graded): F1 0.132, sim share 0.22. FINAL.

## Further minimal pairs
- Row-0 must-block depends on context, not just geometry: 3,4,0,3,3,3,1 = 5.5 (block (0,2)) but 0,3,3,4,5,1 = -3.8 (block (0,2));
  4,3,3,0,6,1 = 3.1 vs 4,3,3,0,4,1 = -0.6 (one stone moved). Centre must-blocks (2,6,1,6,0 = -10; 4,0,5,0,6 = -2) are negative.
- Two must-blocks (opponent already has a double threat) -> -30 to -100 (the negative pole).
- Same board, different move order: 3,4,2,5 = 0.01 vs 3,5,2,4 = 1.39. Unit depends on move history, not only the board.
- Vertical must-blocks inconsistent (5,3,5,3,5 = 1.6; 5,1,5,1,5 = -5.9).
- Mid-band firing (0.8-1.7, the bulk of firing) is mostly late-game boards with few open columns; I found no board rule for it.

## Steer
- 3,3,4,2 max: col3 -8, col2 +6. 3,2,3,4,2,2 max: col3 -5, col4 +3. 134047 max: col3 -4, col0 +6. 68408 max: col3 -11, col6 +6.
  Zeroing has no effect on confident (forced) positions. Effect: pushes probability away from the centre column.

## Synthesis
- 4,3,6,2,3,1 = 6.36, 4,3,6,1,3,2 = 6.35, 3,4,0,3,3,3,1 = 5.54, 6,2,6,3,4,6,3,1 = 5.54, 3,4,1,3,3,3,0 = 5.30. All below dev max 10.02.

## Conclusion
Low confidence. Cleanest component: opponent has 3 of 4 on the bottom row and I must block off-centre (early game).
That covers ~9% of firing at 26% precision. The rest looks like a mixture / history-dependent direction.
