# U38 notebook (layer 0, pole -, thr 0.573, rate 3%)

## Examples (~70 seen across bands)
Nearly all firing positions: my (to-move) stone at bottom-right corner (0,6), early game (ply 2-9),
opponent stones in bottom row (cols 3-5 especially). Late-game firing exists but rare (band 5).

Hypotheses:
H1: grid[0][6]==mine and ply small (<= ~10).
H2: H1 strength scales with count of opponent stones on bottom row (esp. cols 3,4,5).
H3: token-level: I played col 6 early (my first move) + opp moves in cols 3-5.

## Minimal pairs (act)
- Mine at (0,6) is near-necessary: 6,4 -> 0.65 fires; 0,4 / 3,4 etc (no corner) -> ~-0.5. If the corner is the opponent's -> ~0.
- Opp stone ON TOP of my corner stone kills it: 0,6,6 -> -0.94; 6,4,6,4,6,5,6,6 -> -2.42. My own stones above it help a bit (6,4,6,4 1.55).
- Opp bottom-row stones add, by column: 6,c: c0 .51, c1 .29, c2 .03, c3 .53, c4 .65, c5 .59. Opp stones in col 2 hurt (6,4,6,2 0.15 vs 6,4,6,{0,1,3} 1.0-1.2).
- Opp stacked stones in rows 1 also add (6,4,c,4 ~1.0-1.2; 0,6,0 .84).
- My stones in cols 4-5 lower it (0,6,4,5,3 .95 vs 0,6,4,2,3 1.56); my stone at (0,2) slightly raises it.
- Order of moves barely matters (board-based). Decays with ply (6,4,0,0,1,1,2,2,0,0 -> 0.57).
- Rare late-game firings (ply 20-36) not explained.

## Scores
1. p1 corner mine & ply<=9: F1 .571 (P .46 R .75) AUROC .863, sim share .23
2. p2 linear w/o corner gate: F1 .256 (too many FPs) AUROC .871
3. p3 corner gate + col-6 + bottom-row opp weights + ply decay: F1 .607, AUROC .828, sim .31
4. p4 all-rows count weights: F1 .444 (late-game counts blow up) -> abandoned
5. p5 p3 + row-1 stones, thr .5: F1 .588 (R .79) AUROC .883, sim .32
6. p6 col2 -0.5, thr .6: F1 .578
7. p7 = p5 with ply<=12 and thr .62: F1 .679 (P .73 R .64) AUROC .815, sim .32  <- final

## Steer
0,6,4,6,3 / 6,4 / 4,0,3,2,5,6,4 / 6,3,6,3: max or zero changes move probs by <=0.01. No measurable effect.

## Synthesis (all beat dev max 2.203)
1,6,4,2,5,6,4 2.369; 1,6,4,2,3,6,5,6,4 2.297; 1,6,4,2,3,6,5,2,4 2.271; 1,6,4,2,3,6,5 2.260; 4,6,3,2,5,6,4 2.232
