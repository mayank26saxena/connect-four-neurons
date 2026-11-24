# U36 notebook (layer 4, pole +, threshold 0.840, dev max 6.701)

## Observations from examples (bands 0-9, 60 each)
- Firing strongly enriched for column 4 holding exactly one stone (h4==1): band 9 52/60. Second mode: col 4 height 3, esp. opponent vertical three in col 4.
- Bottom cell (0,4) is mine in ~2/3 of top cases; opponent stones at (0,3)/(0,5) common; bottom row "O O X" at cols 2-4 recurring.
- Not mirror symmetric (col 2 analog does not fire).

## Hypotheses
H1: last move stacks on opponent stone (vertical pair) -> rejected by act (3,1,5,4,0 fires; 3,1,6,4,6 no).
H2: column 4 has exactly one stone -> score 1: F1 0.191 (P 0.11 R 0.63), AUROC 0.73.
H3: H2 + neighbour bonuses + col4 OOO -> score 2: F1 0.205, sim 0.03.

## Minimal pairs (act)
- base 3,1,5,4,x: x=5 4.1, x=2 3.2, x=0 2.3, x=6 0.33, x=1 0.06, x=3 0.0, x=4 -0.1. Same position diff order ~same (position-based).
- 4,3,0,3 1.8 vs 4,3,2,3 0.31, 4,3,6,3 1.8, 4,3,5,3 0.36, 4,3,0,3,0,3 (col3 OOO) 0.08.
- 3,4,3,4,x,4 (my XX col3, their OOO col4): 3.1-5.9; 0,4,0,4,6,4 -0.17. Their vertical three elsewhere: no.
- 4,2,1,3,1,1 -> -4.3 (strongly negative), 4,2,0,3,0,0 -> 1.7.
- Steer: negligible move changes (<0.05) on 5 positions.

## Later tests
- Enumerated 4-stone games 4,a,b,c with act (my own synthetic positions): firing ones mostly have their stone at (0,3) next to my single col-4 stone; my horizontal neighbour (0,5)/(0,3) or a second stone of mine on col 4 kills it (down to -3.9).
- 2,4,5,4,x: fires for x in {0,1,2,4,5}, not 3 or 6. Their stone at (0,3) kills here; at (0,2)+(0,5) both needed.
- Not purely heights-based (same heights, different colours differ), not mirror symmetric.
- Firing concentrated in early-mid game (ply 5-20), columns 0 and 6 usually empty.
- Score 3 (neighbour rules): F1 0.174. Score 4 (+ply, edge columns): F1 0.164. Score 5: F1 0.178, sim 0.11. Score 6: F1 0.161.
- Score 7 (p7, combined): F1 0.212 (P 0.14, R 0.44), AUROC 0.68, sim share 0.12. Best. Precision stuck ~0.12-0.14 under every refinement: the selecting factor within "col 4 single stone" was not found; looks like a diffuse/mixed direction.
- Steer: effects tiny (<0.1 prob); zeroing raises column 2 by ~6-8 pts on two strong positions, otherwise <5 pts.
- Synthesis: 3,3,5,4,5,0,2 = 7.20 (beats dev max 6.70); 3,3,5,4,2,0,5 7.17; 3,3,2,4,5,0,5 7.08.
