# U22 notebook (layer 3, pole -; threshold 1.180; dev max 9.752; firing 3%)

## Exploration
- 40 examples across bands + extra band 7/9 samples. ~25% of firing positions are at ply 3 (2nd player to move after 3 stones).
- Full scan of all 343 three-move openings (scan3.txt): 96/343 fire. Strongly left-right ASYMMETRIC (555=5.9 but mirror 111=2.2; 210=5.5 vs mirror 456=0.35; 522=-4.2). O at (0,0) raises it on average.
- Ply 1/2 positions never fire (max 1.07 for 5,5).
- Midgame firing: many top examples have the last O stone on top of an X that sits on an O (vertical O-X-O at column top), e.g. 5,5,5; 53706; 142216; 28743; 136067; 149029; 15358. But 3,3,3,3,3 = 0.03 and 3,3,0,0,3 = 1.3 (counterexamples).
- 8441 (6.49): changing the last move to any other column drops it to <=2.
- Steer (max / zero) on 5,5,5; 0,1,2; 8441; 142216: move probabilities change by <= 0.02. No measurable effect.

## Hypotheses
H1: last opponent stone placed on my stone that sits on their stone (vertical O/X/O at top of last column).
H2: ply-3 opening patterns (opponent stone at (0,0) or bottom-left cluster).
H3: random direction / mixture (asymmetry and opening-specific behaviour suggest this).

## Dev metric log
1. h1 (last O on X on O, vertical): F1 0.061, AUROC 0.517 -> dead.
   (a failed run with `str` NameError did not consume a call.)
2. h2 (ply-3 lookup table of the 96 firing openings from scan3 + last stone in row 2 on my stone): F1 0.182 (P 0.116, R 0.429), sim share 0.05.
3. h3 (ply-3 table + ply>=14 and column 2 has <=1 stone): F1 0.161, AUROC 0.657. Many midgame firings have col 2 (or 3) nearly empty, but so do many non-firing positions.
4. h4 (ply-3 table + opponent has any threat cell in column 2): F1 0.164.
5. h5 (ply-3 table only): F1 0.409 (P 1.00, R 0.257), AUROC 0.628, sim share 0.06. BEST.

## Interpretation
- About a quarter of all firing is at ply 3 (second player to move). The pattern over the 343 openings is left-right asymmetric and not reducible to a simple cell rule (best simple rule "opponent stone at bottom-left cell (0,0)" gets F1 0.57 over uniform openings).
- The remaining 75% of firing is spread over midgame/endgame positions; candidate cues (last stone in row 2, column 2 empty, opponent threat in column 2) each add recall but at precision ~0.1.
- Activation depends mostly on the board (move order permutations barely change it) and strongly on the last move.
- Steer: forcing the unit to max or zero changes move probabilities by <= 0.02 on 4 positions. No measurable single-position effect (although the score's perfect reader ceiling is 61%).
- Conclusion: looks like a mixture / possibly a random direction. Confidence low.

## Synthesis
Greedy 2-move extensions via act. Best 7.03 (1,0,4,4,2,3,3,4,3,6,4); none beats dev max 9.752.
