# U09 notebook (layer 3, pole +, threshold 0.842, dev max 7.421)

## Examples
Top bands: many early positions; bottom row repeatedly shows opponent (O) at cols 1,4,5 and me (X) at cols 3,6,
e.g. ".O.XOOX". Late-game firing positions also have bottom rows like OOOXXOX (O at 1,5; X at 3).
steer: zeroing it barely changes moves (<=0.05).

## Hypotheses
H1: bottom-row pattern: opponent at (0,1),(0,5) (+(0,4)), me at (0,3) (+(0,6)). Perspective-specific, not mirror symmetric.
H2: something about empty col 2 / gap (rejected by minimal pairs: filling col 2 with my stone keeps it high).
H3: last-move driven (rejected: order of moves does not matter, 3,1,6,4,3,5 = 8.0, 3,4,3,5,6,1 = 8.65).

## Minimal pairs (act), ply 5, me={3,6}, them varies
them{1,4,5} 5.5; {1,2,5} 4.0; {1,2,4} 2.7; {0,1,5} 2.2; {2,4,5} 2.05; {0,4,5} 1.46; {0,1,4} 1.17; {0,1,2} .46; {0,2,5} .44
them{1,4,5}, me varies: {3,6} 5.5; {2,3} 3.9; {2,6} 3.4; {0,3} 2.1; {0,6} 1.8; {0,2} 1.0; my stones on top of 1/4 -> 0.8
them{1,5,x}+me{3,6}: x=4 5.7, x=2 4.1, x=0 2.4; them{1,5,6}+me{3,4} 1.16; them{1,3,5}+me{2,6} 1.7
Mirror (them{2,5,1}... me{3,0}) 0.28: not symmetric.
Extra stack on col 3 (my stone at (1,3)) raises to 8.5 (beats dev max): 3,4,6,5,3,1 = 8.51.
My stones on top of their (0,4)/(0,5) lower it (5.0 -> 3.2/2.6).

## Scores
- p1 (bottom-row weights only): F1 0.105 (P .06 R .33), AUROC .59, sim share .02. Pattern too common in non-firing positions.
- p2 (+ -1 per their stone above row 0): F1 0.137 (P .30 R .09), sim .05. Penalty too strong, kills late-game firing.
- p3 (bottom + row-1 cell weights): F1 0.138, sim .04. Misses e.g. ".OXXOXO" (2.7) and "XX.OOOX" (2.4): additive weights inconsistent.
- p4 (bottom weights incl. negatives, -2.5 per their stone on (1,1)/(1,4)/(1,5)/(1,6), +1 my (1,3), -0.25/ply past 7): F1 0.243 (P .28 R .21), AUROC .60, sim .07. BEST.
- p5 (p4, softer ply penalty, graded fires): F1 0.230, AUROC 0.705, sim .07.

## Other findings
- Band histograms of bottom row (band 9 vs band 0): X at col3 78% vs 52, X at col6 78 vs 40, O at col1 81 vs 41, O at col5 77 vs 36, O col4 62 vs 43; O at col3/col6 ~0-7%.
- Late-game firing (ply>=16, ~30% of firing): same bottom row, plus stack structures (my (3,3) 94%, their (2,5) 84%, my (1,5) 86%), and
  jumps triggered by single upper stones (e.g. their stone at (2,6) took 0.2 -> 3.4). Not captured by a simple rule.
- Their stones on row 1 above the pattern (cols 1,4,5,6) cut activation from ~6 to ~2; my stone at (1,3) raises it (to 8.4).
- Activation flips with perspective (alternates between plies as the side to move changes).
- Not mirror symmetric; move order irrelevant.
- steer: effect negligible (<= 0.09 probability change in 4 positions).
## Conclusion
Diffuse, perspective-specific bottom-row configuration detector with poorly understood late-game contributions; possibly a random direction. Confidence low.
## Synthesis
3,4,3,5,6,1 (8.65), 3,4,6,5,3,1 (8.51), 3,1,6,5,3,4 (8.45), 1,3,4,6,5,3,0 (8.44), 3,1,6,4,3,5 (8.03): all beat dev max 7.42.
