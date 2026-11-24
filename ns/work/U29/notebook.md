# U29 notebook (layer 0, pole -, threshold 0.800, dev max 2.812)

## Examples (40, all bands)
Every firing example (bands 5-9) has last move in column 3, never in row 0, mostly mid/late game (ply 14-28).
Band 3-4 (just below) are also last-col-3 positions, often earlier ply.

## Hypotheses
H1: last move col 3 stacked on top of something (last_row >= 1), late enough ply.
H2: depends on ownership of col 3 stones: needs my (X) stones in col 3 under the opponent's last stone.
H3: depends on whether previous move was also col 3 (stacking pair).

## act tests (base = 0x6,1x6, 12 plies)
- base,3 (row 0): 0.03. First stone in col 3 always low/negative (-1.7 at ply 3).
- base,3,3 (X under O): 0.89 fires; base,3,2,3 (O,O in col3): 0.25; base,4,3,4,3 (O,O): -0.02. -> H2 supported.
- base,3,2,2,3 (X,O, prev move not col3): 1.14 fires -> H3 not needed.
- base,3,2,3,3 (X,X,O): 1.45 ; more X in col3 -> higher.
- all-O col3 stacks (alternating 3,2) late: 0.46-0.70, below threshold but elevated.
- ply effect: same 3,3 pattern at ply 4: -0.12, ply 6: 0.23, ply 10: 0.66, ply 12: 0.85, ply 14: 0.9-1.2.

## More act tests
- Token bag, order-insensitive: 0x6,4x6 vs 4x6,0x6 same (0.09 vs 0.07). Column/owner of other stones shifts the level:
  12-stone prefixes (balanced owners) before 3,3: cols0/1 0.89, 0/6 0.68, 0/2 0.57, 0/5 0.58, 1/6 0.34, 0/4 0.09, 2/4 -0.81.
  Owner matters too: me-in-col0/them-in-col1 0.885 vs them-in-col0/me-in-col1 0.387. Context-dependent (softmax-like), not cleanly additive.
- More of my stones under the last col-3 stone raise it up to 2-3 (X,X,O 1.33-1.47), 4 mine lowers again (1.06).
- Ply effect saturates at ~14-16 stones outside col 3.

## Dev metric
- v1 (last col3, row>=1, >=1 mine below, ply>=12): F1 0.600 (P 0.43 R 0.98), AUROC 0.969, sim share 0.64. (call 1 output lost by piping; call 2 = same file)
- v2 (linear score: 0.1*min(other,14) + col3 mine/theirs bonus + small column weights, thr 0.8): F1 0.694 (P .56 R .91), sim 0.59
- v3 (stronger col weights, saturating mine bonus, thr 0.8): F1 0.629 (P .71 R .56), sim 0.61
- v4 (= v3 with thr 0.62): F1 0.702 (P .62 R .80), AUROC 0.894, sim 0.61  <- BEST
- v5 (v3 without column weights): F1 0.632, sim 0.58 -> column weights help precision.
Remaining errors: near-threshold positions where the mix of other columns/owners moves the value by +-0.3; not captured simply.

## Steer
Three positions (act 1.3, 1.2, 2.1): forcing max or zero changes move probabilities by <= 0.02. Effect: none measurable.

## Synthesis
Best: 0,1,0,1,0,1,2,5,2,5,2,5,3,6,3,6,4,4,6,4,3,3 = 3.18 (dev max 2.81). Recipe: my stones in col 2 and col 3, opponent stones in col 5/6/4, ~20 plies, last move = their stone on top of my col-3 stones.

## Synthesis revision (orchestrator audit, after submission)
Audit found 4 of 5 synthesis sequences completed a four-in-a-row (two at move 7, vertical in col 0; two at move 22, P2 anti-diagonal (0,6)-(3,3)).
I checked every move with ns/work/U29/legal4.py, a validity checker that tests only whether a move completes a four and scores nothing. Kept the one valid original and replaced the other four. Only `synthesis` and one line of `notes` were changed; no score calls.
- 0,1,0,1,0,1,2,5,2,5,2,5,3,6,3,6,4,4,4,6,3,3  2.816 (kept)
- 0,1,0,1,0,1,2,5,2,5,2,5,3,6,3,6,4,4,3,3      2.919
- 0,1,0,1,0,1,2,6,2,6,2,6,3,5,3,5,4,4,4,5,3,3  2.914
- 0,1,0,1,0,1,2,5,2,5,2,5,3,6,3,6,4,4,4,4,3,3  2.912
- 0,1,0,1,0,1,2,6,2,6,2,6,3,5,3,5,4,4,3,3      2.899
All beat the dev max of 2.812. The best valid value, 2.92, is lower than the invalid 3.18.
