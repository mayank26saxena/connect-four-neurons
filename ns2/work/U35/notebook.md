# U35 notebook (layer 0, pole -, threshold 0.632, dev max 1.417)

## Observations
- Top band dominated by ply-4 positions where the last (opponent) move is in col 5/6 (or 4), rows 0-1, with stones mostly on right side.
- Activation is very ply dependent: high at ply 1-4, decays later. Left/center-heavy games go negative.
- Ply-2 grid: last move col 5 strongest (~1.2-1.8), col 6/4 next, col 3 / col 1 weakest.
- Stacking: last stone at row >= 2 kills it (4,5,5,5 0.34; 5,5,5,5 -0.48; 4,5,6,5 1.42).
- Prefix full of cols 0-3 then last move in col 5: ~0.0-0.5 (no fire).
- Midgame exceptions: 1,4,5,3,3,3,3,2,1,4,4,4,5,6 -> 1.23 (last 6 at row 0); last 0 at row 0 -> 0.09.

## Hypotheses
H1: early game (ply small) + last move in cols 4-6 at row 0-1 + most stones on the right side (cols 4-6).
H2: graded sum: last-move column weight + right-side fraction - ply penalty.
H3: position-specific mixture (layer 0, token-averaging) -> may be low confidence.

## score 1 (p1: last col 4-6 row<=1, ply<=14, right-side majority): F1 0.251, P 0.227 R 0.282, AUROC 0.626, sim share -0.21. Poor.

## Minimal pairs at ply 4 (additive, order-independent for earlier stones, last move special)
- my stone weight (vs col 1 = 0): c0 ~+0.2, c2 +0.1, c3 0, c4 +0.42, c5 -0.23, c6 +0.62
- their earlier stone: c0 -0.35, c1 0, c2 -0.24, c3 -0.33, c4 0, c5 0, c6 +0.09
- last (their) move column: 0:0, 1:.2, 2:.1, 3:.05, 4:.4, 5:.75, 6:.55; penalty ~0.3 per row of landing.
- later in game contributions are diluted (layer-0 averaging) plus ~-0.03/ply drift.
H2 implemented as a hand-set additive score (p2).

## score 2 (p2 additive hand-set weights): F1 0.179, P .30 R .13, AUROC .56. Worse; misses include high-row last moves in col 3 (0,1,4,5,4,4,6,3,4,3,3,3,3 -> 1.21). Additive board model fails; activation swings strongly ply to ply (odd/even alternation in some games), sequence-dependent.

## score 3 (p3: ply<=6, last col>=4, col3 short): F1 0.205. Dropped last-move idea.

## Breakthrough: per-band column-height histogram
Band 9: col 0 empty 87%, col 2 empty 90%; band 0: 21%/14%. Col 1 often occupied in firing positions; col 5 nearly always occupied (empty 5%).
H4: columns 0 and 2 both empty (left even columns untouched), with decay as ply grows.
Minimal pair: 3,3,4,5,5,4,3,3,6,6,1,1,4,4,5,5,6,6,1 + 1 -> 0.39 vs + 2 -> -0.40; game with 0/2 untouched fires through ply 17, fades after ~ply 20.

## score 4 (p4: h0==0 and h2==0 and ply<=18): F1 0.311, P .25 R .41, AUROC .68. Best so far.
FPs: col 1 stacked, right side empty (1,3,1,1,3 -> -0.19). Misses: last move strong in cols 1/3/4/6 with a stone in col 0/2.
## Grid probe base 3,3,4,5,5,4,3,3 + (x me, y them last):
last y: 0 ~0, 1 +.5, 2 ~0, 3 +.6, 4 +.6, 5 +.35 (row 2), 6 +1.0. Earlier x: 0 0, 1 +.15, 2 -.2, 3 -.05, 4/5 +.05, 6 +.2.
-> the last move's column dominates (not in 0/2, best 6/5/4), plus board-wide left-even emptiness, decaying with ply.

## score 5 (p6: last-col weight + (right - 2*(h0+h2) - h1)/ply - ply drift): F1 0.300, AUROC .69, sim share 0.06.
## score 6 (p7: p6 + bonus when cols 0 and 2 both empty + strong penalty when last stone lands row>=2 in cols 4-6): F1 0.341 (P .31 R .37), AUROC .67, sim share 0.11. Best.
Remaining misses: odd sequences like 0,1,0,5 (0.86), 2,1,6,5 (0.94); activation alternates ply to ply in some games -> sequence/token-level layer-0 mixture.
## steer: max/zero on 4 positions (4,5,6,5; 3,3,4,5,5,4,3,3,6,6; 0,1,4,5,4,4,6,3,4,3,3,3,3; 3,3,4,5,5,4,3,3,6,6,1,1,4,4): all changes <= 0.01. Effect none measurable (sim ceiling only 19%).
## synth: 6,5,4,5 = 1.421 beats dev max 1.417; 4,5,6,5 / 6,4,4,5 / 4,4,6,5 ~1.414-1.417; nothing much higher found at ply 4-6.
Conclusion: early-game, right-side, left-even-columns-empty detector; mixture; confidence low (F1 < 0.4).
