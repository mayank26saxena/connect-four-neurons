# U77 notebook (layer 1, pole +, threshold 0.333, dev max 3.261)

## Observations (examples, 100+ firing positions read)
- Strong firing (band 8-9) almost always: odd ply (me = second player), my stone at bottom-left corner (0,0),
  opponent stones at bottom-right (0,5)/(0,6). Often (0,4) empty.
- Weak firing near threshold (band 5-6): many even-ply ply 4-6 positions with my stone at (0,1).

## Hypotheses
H1: odd ply & mine at (0,0) & theirs at (0,6) or (0,5).
H2: weighted sum over bottom-row cells (mine-left +, theirs-right +, theirs (0,4) -, mine (0,1)/(0,4) -), gated by parity.
H3: purely absolute colour (P2 at a1, P1 at g1) regardless of side to move. Rejected-ish: 6,0,3,3 (P1 to move) = 0.04.

## Minimal pairs (act)
- 6,0,3,3,5 = 1.71; move my 0 -> 1: -0.55; -> 2: 0.72; -> 4: -1.40.
- their 5 -> 4 (6,0,3,3,4): -0.08; their 5->2: 0.33; 5->1: 0.45. 5,0,3,3,6: 1.13.
- swap sides 0,6,3,3,5: -0.02. Even ply 6,0,3,3: 0.04; 0,6,3,5 (me at 0, them at 5,6, even): 0.06 -> parity matters.
- 6,0,3,3,5,5 (them stacks to (1,5) ... actually me plays 5 -> mine at (1,5), even): 0.03.

## More minimal pairs
- Their stone at b1 next to my a1 boosts: 6,0,1,2,5 (X O X . . O O) = 3.28. My stone at e1 hurts (6,0,1,4,5 = 0.93), their e1 hurts.
- My stone on top of their b1 (b2) kills: 6,0,1,1,5 = 0.30; their stone on a2 lowers (6,0,3,3,5,3,0 = 0.85).
- Adding stones above decays it: col-3 stacking on 6,0,1,2,5: 3.28, 2.32, 2.38, 1.71, 0.70, 0.66, 0.14 at ply 5..17. Even plies ~0 throughout.
- Mostly board-driven (6,0,3,3,5 == 3,0,6,3,5) but move order still shifts it up to ~1 (1,4,5,0,6 = -0.21 vs 6,0,1,4,5 = 0.93).
- Even-ply firing (about a third of firing mass, mostly near threshold, ply 4-6): same pattern from mover's view only gives ~0.5; absolute-colour flip gives 0.

## Score log
- s1 H1 boolean (odd, a1 mine, f1/g1 theirs): F1 0.153 P 0.095 R 0.40; sim share 0.02.
- s2 bottom-row weights, parity: F1 0.199; sim 0.03 (FPs are tall boards).
- s3 + strong dilution 0.25/stone above row 0: F1 0.141 P 0.85 R 0.08; sim 0.10.
- s4 column-presence weights + ply dilution: F1 0.211; sim 0.07.
- s5 cell weights + row-1 terms + dilution 0.1 + ply-4 rule: F1 0.260; sim 0.13.
- s6 drop ply-4 rule, soften e1, thr 2.7: F1 0.297; sim 0.09.
- s7 thr 2.4: F1 0.328 P 0.40 R 0.28; sim 0.10. FINAL.

## Steer
- 5 positions, to max and to zero: changes <= 0.01 in every column. No measurable effect on move.

## Synthesis
- 3,2,6,0,1,3,5 = 3.55; 3,3,6,0,1,2,5 = 3.53; 3,3,1,0,6,2,5 = 3.52; 3,0,6,3,1,2,5 = 3.45; 1,0,6,2,5 = 3.30 (dev max 3.26).

Conclusion: dense, weighted bottom-row pattern; F1 0.33, so low confidence.
