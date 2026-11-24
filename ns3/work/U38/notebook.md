# U38 notebook (layer 5, pole -, threshold 0.851, dev max 21.08)

## Examples (60+ viewed)
- Band 9 (12-21): ALL are an open three on the BOTTOM ROW (_OOO_ or _XXX_) with both end cells empty -> two playable
  winning cells in row 0 (either my wins or their must-blocks). Early game (ply 5-9).
- Band 8: same, plus a few bottom-row split threes and "XX with open bottom row" (4,4,3,4 -> 5.9).
- Bands 5-7 (0.85-4.4): mixed; many late-game positions with vertical threes (must-block near top), some bottom-row pairs.

## Hypotheses
H1: row-0 double threat (open three on bottom row) -> very high.
H2: row-0 pair of same colour with empty bottom-row space around (can become open three) -> moderate.
H3: generic must-block / threats -> weak contribution.

## act tests
- 2,6,1,6,3 (OOO 1-3, 0 and 4 empty) 15.3; 2,6,1,0,3 (0 blocked, single threat) -0.86 => DOUBLE threat needed.
- Elevated open three in row 1 (1,2,3,4,5,2,0,3,6,4) 0.01 => bottom row specific.
- Single row-0 threats vary: -0.6 .. 4.3 (location/other stones dependent).
- XX at 3,4 row 0: with opponent stacked on top (3,3,4,3) 6.6, (4,4,3,4) 5.9; with opponent stones on row 0 at 0/6 (3,0,4,6) 0.27, (3,6,4,6) -1.0.
  So opponent stones on the bottom row kill it; the pattern wants an otherwise-empty bottom row.
- Vertical threes: 0.1-1.6, inconsistent.
- steer: lost positions (open three for them) no change; 4,4,3,4 max-steer moves prob from col5 to col2 (+0.17); forced wins unchanged.

## Score log
1. p1 row-0 open three + row-0 open-pair setup: F1 0.155 (P .54 R .09), AUROC .54, sim share .11. Firing is much broader.
2. p2 any immediate win / must-block: F1 0.229 (P .13 R .77), AUROC .81. Threats are a necessary-ish ingredient but most threat positions don't fire.
3. p3 any playable win cell on the bottom row (either side): F1 0.334 (P .49 R .25), sim .15.
4. p4 p3 + bottom-row open-three setup: F1 0.332 (no gain).
5. p5 p3 + must-block in cols 2-4 (any row): F1 0.335 (P .23 R .61).
6. p6 p3 + must-block above row 0 in cols 2-3: F1 0.365 (P .28 R .53), AUROC .74, sim .15. BEST.
7. p7 p6 with cols 1-4: F1 0.290 (worse).

## Further act findings
- Bottom-row pair setups fire for some placements (2-3, 3-4, 4-5, 1-3, 3-5) but not others (1-2, 2-4, 0-1, 5-6); no clean rule.
- Vertical threes: opponent's three (must-block) fires sometimes (col2 1.6-3.9) depending on unrelated stones; my own vertical win does not (-0.5).
- Single bottom-row threats: mine usually fire (2-11), theirs usually not (-1.5..0.4) but examples exist both ways.
- Left/right asymmetric (mirror of 4,0,5,0,6,0 = 4.3 is 0,6,1,6,2,6 = -0.35).
- Ply parity histogram by band: flat.

## Steer
- Lost / forced positions: no change. With two winning bottom-row moves (3,0,4,0; 4,4,3,4) forcing the unit high shifts ~0.2 prob from col 5 to col 2. Otherwise negligible.

## Synthesis
- 4,4,5,4,3,0 (my open three cols 3-5, both ends empty, opponent stacked on col 4 and col 0): 21.72, beats dev max 21.08.

## Conclusion
Clean, very strong part: bottom-row open three (two playable winning cells on row 0) -> top activations. The firing threshold region (0.85-3)
is a diffuse mixture of other immediate threats (mostly must-blocks in central columns, some single bottom-row threats). Confidence low (F1 0.365).
