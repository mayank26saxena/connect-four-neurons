# U35 notebook (layer 0, pole +, thr 0.002, dev max 0.006)

## Exploration
- Top bands (7-9): overwhelmingly last move in column 3 (centre). Many are ply-4 openings like x,0,y,3. Band 6 has many ply-1 "1" openings (first move col 1 -> 0.002, just at threshold).
- act: 0,0,5,3 = 0.005; a,b,c,3 at ply 4 almost always fires (4,4,5,3 and 6,0,6,3 don't). Ply 2/3 with col-3 last don't fire.
- Long filler prefix ending with 3: activation alternates by parity and drifts down with ply; penultimate move matters slightly (6 lowers).
- Late-game col-3-last positions also fire in dev.

## Hypotheses
H1: last move was in column 3 (centre).
H2: H1 plus ply-dependent modulation (ply 4 strongest).
H3: plus first move "1" at ply 1.

## Tests (act)
- Ply-4 col-3-last fires for almost any first three moves (5,5,x,3 / x,5,5,3 / 5,x,5,3 all 0.002-0.004); 4,4,5,3 and 6,0,6,3 are exceptions.
- Same filler prefix ending in 3: activation alternates with parity and drifts down with ply -> strong position-embedding dependence.
- Late game (ply ~30-36): even plies (me = first player) fire for almost any last column (2,4 best; 0/6 weaker); odd plies are strongly negative (-0.02 to -0.03, esp. after a col-0 move). Amplitude grows with stones in the edge columns 0 and 6.
- Synthetic random-ish games (short, centre-weighted) almost never fire (2/2881 positions): firing depends on long, edge-filled engine-like games.

## Dev metric
1. last_col==3: F1 0.124 (P .074 R .378) AUROC .618, sim 0.47
2. ply1 col1 | ply4/5 col3 | even ply>=24 & last in 3-6: F1 0.294 (P .187 R .684) AUROC .797, sim 0.56
3. as 2 but late rule = even ply>=20 & edge stones (h0+h6)>=9: F1 0.340 (P .229 R .658), sim 0.58
4. additive hand score >=6: F1 0.317 (P .197 R .814) AUROC .857, sim 0.42
5. same, threshold 8: F1 0.272, sim 0.03 (worse)
6. 3 + exclude last_col 0 in late rule: F1 0.369 (P .263 R .623) AUROC .785, sim -0.39 (level changed; simulation unstable)
7. 6 fires with 3's level: F1 0.369, sim 0.58  <- final

## Steer
0,0,5,3 (max): no change (<0.01). 3,3,4,2 (max): no change. Late game ply 32 (zero): no change. 2,4,6,3,1,1,0 (max): no change. Effect none measurable (activation range is tiny, max 0.006).

## Synthesis
Best 0.005 (0,0,5,3; 1,0,0,3; 1,0,3,3; long game ending ...0,4 at ply 32). None beat dev max 0.006.

## Conclusion
Looks like a layer-0 mixture of token/position effects (last token col 3, ply 4, ply parity, count of edge-column tokens), no clean board concept. Low confidence.
