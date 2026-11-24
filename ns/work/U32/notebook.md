# U32 notebook (layer 3, pole -, threshold 0.906, dev max 10.875)

## Observations (examples, bands 0-9)
- Top examples: columns 2 and 4 stacked 3+ high, column 3 low/empty, columns 0-1 low.
- Single-cell histograms band 9 vs band 0 (60 each): enriched (1,4)=me 54/60, (1,2)=them 52, (0,5)=them 49,
  (2,4)=them 48, (2,2)=me 42, (1,5)=me 40, (0,2)=me 41, (0,4)=them 40; empties at (1,0),(1,1),(2,0),(2,1) ~all,
  col 3 low ((1,3),(2,3) empty). Depleted: (1,2)=me, (2,4)=me, (1,5)=them, (0,5)=me.
- Strongly perspective-dependent: after ANY move the activation collapses (colours swap).

## Hypotheses
H1: checkerboard pattern on cols 2/4/5 around rows 0-2: col2 me/them/me (rows 0-2), col4 them/me/them, col5 them/me,
    with col 3 and cols 0-1 empty. Unit = graded template match.
H2: one key cell, e.g. (2,2)=me on top of (1,2)=them (gating).
H3: column-3 "hole" between tall cols 2,4 regardless of colours. -> rejected: colour swap kills it.

## Minimal pairs (act)
- 4,2,4,2,2,4 (core col2 T,T,M / col4 M,M,T): 0.63; adding (0,5)T: 2.8; +(1,5)M: 5.9.
- 2,4,4,5,5,2,2,4 (full H1 template): 4.3; +6,6: 6.8.
- 2,4,4,5,5,6,2,4 ((1,2)=me instead of them): -0.63. (1,2)T matters.
- 2,4,4,2,6,5 (no (2,2)M): -0.79; same +(2,2)M,(2,4)T: 3.5 -> (2,2)M strong.
- 4,5,4,4,5,2,6,1 (no col2 stone above row 0) 3.45: col4 M,M,T + col5 T,M + (0,1)T + (0,2)T enough. H2 not necessary.
- 2,2,2,4,4,5,5,x: x=0 4.0, x=1 ((0,1)T) 6.7, x=3 ((0,3)T) 1.7, x=2 1.7, x=6 2.4; stacking col 0 kills (0.7).
  (0,3)=me +: 7.1.
=> Distributed, roughly additive cell template (H1), with col 0/1 stones and col-3 'them' stones suppressing.

## Dev metric log
- call 1 (p1, single template, thr 7): F1 0.280 (P 0.48 R 0.20) AUROC 0.60, sim share 0.23.
- call 2: accidental duplicate of call 1 (same program) - wasted.
- call 3 (p2, re-weighted template incl. col-3 cells, stack penalty cols 0/1, thr 6): F1 0.451 (P 0.45 R 0.45) AUROC 0.72, sim 0.32.
- More minimal pairs: base 2,4,4,2,2,4 + (me at row0 c, them at row0 d): me (0,1)+, me (0,0)-, them (0,0)/(0,3)-, them (0,5)+, me (0,6)+.
  2,4,4,2,6,5 (no row-2 stone in col 2 or 4) is -0.79 even though the template rates it high -> the left part (cols 1-2)
  and right part (cols 4-5) seem to combine like an AND, not a sum.
- call 4 (p4, left/right halves + row-2 anchor + penalty for stones in rows 4-5): F1 0.429 (P 0.64 R 0.32), sim 0.33.
- call 5 (p5, stronger col 0/1 penalties): F1 0.441 (P 0.68 R 0.33), sim 0.39.
- call 6 (p6, anchor dropped, halves thresholds loosened): F1 0.499 (P 0.61 R 0.42) AUROC 0.71, sim 0.43.
- call 7 (p7, thresholds lowered again): F1 0.517 (P 0.54 R 0.49) AUROC 0.74, sim 0.43.  <- final
- Misses are partial versions of the pattern (e.g. col 3 alternating, or only the right half), so the unit looks
  like a distributed fixed-cell colour template rather than one crisp concept.

## Steer
- Effects are small. Zeroing at 8.4 (159557): col 3 +0.08, col 0 -0.09. Forcing max at 2,4,4,2: col 3 -0.09, col 2 +0.09.
  At 56113 zeroing: col 2 +0.06, col 1 -0.05. Others under 0.03. So when active, the unit slightly suppresses column 3.

## Synthesis
- 2,4,4,5,5,2,2,4,3,1,6,5 = 13.5 (dev max 10.9). Others 12.0-12.5. Recipe: col2 me/them/me, col4 them/me/them,
  col5 them/me/them, (0,1) them, (0,3) me, (0,6) me, everything else empty.
