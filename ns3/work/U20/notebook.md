# U20 notebook (layer 5, pole -, threshold 0.938, dev max 44.2)

## Examples
- Bands 7-9 (act 7-44): almost all have opponent must-block in COLUMN 2; top band = opponent vertical three in col 2 (last move col 2), cell above empty.
- Band 7 also diagonal threats landing in col 2 (100845 act 10, 128545 act 7).
- Bands 5-6 (0.94-3.7): mixed, many have no must-block at all. Unclear.

## Hypotheses
H1: opponent has an immediate (playable) win in column 2 (vertical strongest, diagonal next).
H2: horizontal col-2 threats do not count.
H3: low-band firing is something else / noise.

## Minimal pairs (act)
- 5,4,1,2,2,1,2,4,2 (O vertical 3 col2) = 33.7; same in col3 = -0.42, col0 = -0.43; last move 3 instead = -0.36.
- 0,2,0,2,6,2 = 18.0; same pattern in col 1/3/4/5 = ~0.
- Horizontal three O at row0 cols 3-5 with (0,2) open: 0.11-0.23 -> horizontal does NOT fire.

## Score log
- s1 p1 (any col-2 must-block, vertical 9 / diag 6): F1 0.423 P 0.571 R 0.337 AUROC 0.664. FPs = diagonal col-2 threats at rows 1,3,4 (act 0.3-0.6).
- s2 p2 (+require row>=2 for non-vertical): F1 0.433 P 0.555 R 0.356.
- s3 p3 (any their threat cell in col 2, playable or not): F1 0.162 P 0.098 -> non-playable col-2 threats do NOT drive it. Dropped.
- s4 p4 (vertical three in col 2, or must-block exactly at (2,2) any direction): F1 0.492 P 0.799 R 0.356.
- s5 p5 (p4 but not when opponent has 2+ must-blocks; level +1 for col2 height 2): F1 0.498 P 0.839 R 0.354; sim -113.6% (vs perfect -70%), odd metric.
- s6 p6 (p5 fires, level without the height-2 term): F1 0.498 P 0.839 R 0.354; sim -45.0% (perfect -70%, share nan). Chosen.

## Extra minimal pairs
- Diagonal O threat at (2,2) built from scratch (3,3,3,3,1,1,6,0,6,2,2,5) = 3.58; mirror to col 4 = 0.07.
- Horizontal O three at row 2 into (2,2) = 1.29 (weak fire); horizontal into (0,2) = 0.1-0.2.
- O threat directly above an empty col-2 landing (row 1) = ~0: "poisoned col 2" does not fire.
- Col-2 height 2 alone (3,3,2,2 etc.) = ~0.

## Residual
- ~1150 misses are near-threshold firings (act 1-4), early-middle game, col 2 often height 2, no shared tactical feature found;
  the model does not play col 2 there (p(col2) ~0.00-0.04). Treat as diffuse/weak.

## Steer
- to max: col 2 jumps to 0.84-1.00 in 5 positions (+0.16 when start position quiet); to zero: no change (redundant with other circuitry).

## Synthesis
- X,X at bottom of col 2 then O,O,O above (threat at (5,2)): 2,4,2,2,4,0,6,2,1,2 = 45.3 (> dev max 44.2), 4 sequences beat dev max.
