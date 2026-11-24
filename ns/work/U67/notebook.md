# U67 notebook (layer 4, pole -, threshold 1.146, dev max 13.666)

## Exploration
- 40 examples + 300-sample histogram (ex300.txt). Column 1 empty in 55/68 positions with act>3, 35/82 in 1.1-3, vs ~18% of non-firing.
- Strong parity dependence: act flips between moves (e.g. 6,4,5,3,3 = 6.3; +4 = 0.13; +4 = 13.7 = dev max).
- Minimal pairs on 6,4,5,3,3(,4,4): an opponent (O) stone at bottom of col 1 or col 2 kills firing; my stone at (0,2) boosts (10.7);
  my stone at (0,1) only weakens. My stone at (2,3) or (1,5) kills in the 7-ply position. Steering effects tiny (<=0.1).

## Hypotheses
H1: column 1 is empty (simple, broad).
H2: column 1 empty and no opponent stone at the bottom of columns 1-2 / left region (refinement).
H3: something about the opponent's potential lines through the empty left-bottom area (mover's open left side).

## Tests (act minimal pairs; ga.sh/g2m.py build a move order for an edited grid)
- 13.666 base (6,4,5,3,3,4,4 = "...XXOO/...OX../....O.."): adding one O stone anywhere except the bottom of col 1/2 keeps it firing (2.7-13.2);
  an O at (0,1) or (0,2) kills it (~0). X at (0,2) boosts; X at (0,1) weakens; X at (0,1) in 56054 kills.
- Color swap of 56054 kills firing (8.5 -> -0.1); mirror image of the 6,4,5,3,3 core does not fire -> left-side and color specific.
- 5427: filling the second hole (col 4) also drops 7.7 -> 1.3, so "two separate empty columns" matters in some positions.
- Strong dependence on who moved first: early-game firing is mostly second player to move (30% me_first), late-game (ply>=30) 92% me_first.
- Per-cell maps (col1-empty subset): firing has O at (0,2) 12% vs 46% non-firing; X at (1,2) 12% vs 42%; col 3 has O stones.

## Dev metric
1. p1 col1 empty & ply>=5: F1 0.165 (P 0.098 R 0.50) AUROC 0.679, sim 0.03
2. p2 col1 empty & O in col3: F1 0.174, AUROC 0.659, sim -0.02
3. p3 col1 empty & (0,2) not O & h3>=2 (& ply>=5): F1 0.194 (P 0.14 R 0.31) AUROC 0.626, sim -0.05  <- best F1
4. p4 p3 + h2<=1: F1 0.131 (worse; misses with col 2/col 5 empty)
5. p5 any deep well column: F1 0.087 (far too broad)
6. p6 left-clear + parity by phase: F1 0.154
7. p7 p3 + a low column on the right: F1 0.173
Conclusion: nothing exceeds 0.2. The unit's top regime is clear (col 1 empty, no opponent stone at bottom of cols 1-2, opponent stones in col 3-4, often a second hole on the right) but the
threshold band is a mixture (late-game deep wells, parity), so confidence low.

## Steer
Forcing to 0 or max moves probabilities by <=0.1: 13.666 pos zero -> col2 +0.07, col3 -0.05; 0,3,3,4,2 max -> col3 -0.10, col2/col4 +0.06; 60584 zero ~0. No consistent large effect.

## Synthesis
6,4,5,3,3,4,4,2,5,5,4 = 16.59 (beats 13.666); 6,4,5,3,3,4,4,2,5 = 15.64; 6,4,5,3,3,4,4,2,5,6,4 = 14.83; 6,4,5,3,3,4,4,2,4 = 14.11; 6,4,5,3,3,4,4 = 13.67.
