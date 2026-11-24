# U23 notebook (layer 4, pole +, threshold 1.316, dev max 6.659)

## Observations (examples, ~60 firing boards)
- Band 9 (top 0.1%) almost entirely: a bottom-row (row 0) horizontal open three, cols 3-5 (ends 0,2 / 0,6) or cols 1-3 (ends 0,0 / 0,4), either player's. Double threat on row 0.
- Bands 5-8 diverse: ~37% have a must-block; many have none. Early (ply 3) firing: opponent stones at bottom cols 3 and 6 (6,2,3 / 3,2,6 / 6,0,3).
- Steer: in lost positions the policy is ~uniform, steering changes nothing (<0.03).

## Hypotheses
H1: fires when there is an immediate win/must-block (esp. two of them = double threat on row 0).
H2: bottom-row horizontal pattern detector (opponent/any stones in row-0 windows), weighted to threat cells at even cols (0,2,4,6).
H3: random direction / mixture.

## Minimal pairs (act)
- 3,0,4,0,5 (O row0 cols3-5, ends open) 2.93 FIRES; 3,0,4,6,5 (end (0,6) blocked by me) -1.06; 3,6,4,1,5 -0.90.
- 2,0,3,0,4 (O cols 2-4, ends 1,5 open; still a double threat) only 1.19 (no fire!). 1,0,2,0,3 (one end blocked) -0.73.
- 3,3,4,4,5 3.36 FIRES.
- ply-3: O at bottom 3&6 fires (~1.3-1.5) regardless of my stone col 0/1/2; O at 2&3 0.7-1.0; others <0.3.
- 1,1,0,6,1,2,5,2,1,2 (opp makes vertical three in col 2, must-block (3,2)) 1.67 FIRES; any other last move <=0.46.

## Score calls
- call 1 (accidental duplicate run of p1, counted as 2 calls): p1 = any immediate win / must-block: F1 0.102 (P 0.061, R 0.312), AUROC 0.584, sim 0.01. H1 rejected.
- call 3, p2 = row-0 open three OR >=5 full columns: F1 0.145 (P 0.10, R 0.24). Endgame alone not it.
- More probes: asymmetric under mirror (left/right) in most cases (e.g. 6,2,3 1.47 vs mirror -0.20). Ply-3 grid: opponent stones in cols 2,3,6 raise it, my stone at col 0 lowers it. Looks like a diffuse, cell-weighted feature.
- Late-game: in two fired positions the last move filled an edge column and left the mover with only losing moves (engine -966); alternatives where the mover can win were ~0. Suggested H6 "mover is lost".
- call 4, p3 = every legal move lets the opponent win at once (lost within 2 plies): F1 0.219 (P 0.273, R 0.183), sim 0.01. Best precision so far, low recall.
- call 5, p4 = p3 OR row-0 open three (either colour, both ends empty) OR I have >=2 immediate wins: F1 0.224 (P 0.246, R 0.205), AUROC 0.593, sim 0.01.
- Teacher-score check on 45 fires vs 45 non: fires lost for mover 11/45 vs 7/45, won 1/45 vs 7/45. Most fires are ordinary positions with no visible tactical feature.

## Steer
- 3,0,4,0,5 (lost) max: all changes <=0.01. 6,2,3: <=0.01 both ways. 0,2,0,2,3,5,0,0,3,5,5,3,3: max moves 6 pts from col 2 to col 3 (+0.04); zero does the reverse (+0.03 col 2). Late forced positions: 0. Effect is essentially nil.

## Conclusion so far
Top 0.1% is clean (bottom-row open three with both ends empty, mostly cols 3-5 or 1-3, much weaker for 2-4). The other ~97% of firing is diffuse and asymmetric with no clean board concept. Looks like a mixture or a random direction -> confidence low.

## Synthesis
Greedy 2-move extensions of a row-0 open-three position (O at cols 1-3, ends 0 and 4 open, plus a column-2 threat): best non-terminal 2,6,1,6,5,1,3,3,3,6,6,5,2,6,2 = 5.96 (dev max 6.66). Higher values (6.35) only came from positions where the opponent had already made four, so I dropped those.

## Final
p4 (F1 0.224, sim 0.01), confidence low.
