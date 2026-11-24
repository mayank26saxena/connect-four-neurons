# U83 notebook (layer 2, pole -, threshold 0.629, dev max 3.529)

## Observations
- Band 9: col3 height 1-2 in ~all (h3 in {1,2}: 59/60), lower bands ~15-25%.
- Col3 contents (mover view, bottom-up): 'OX' dominates top band (67/120), then 'X', 'O', 'XX'.
- Last move rarely in col 3 at top. Last move cell (3,5) and (0,0) over-represented in band 9.
- Minimal pairs: 6,3,3,0 = 2.95; 6,3,3,3 (third stone in col3) = -0.07; 3,3,0,6 (col3 XO) = 0.3.
  6,3,3,x fires for every x != 3. But 1,1,5,3,3,0 (col3 OX) only 0.2: context-dependent.
- 5,5,5,0,5 = -0.95 vs 3,5,5,5,5 = 2.7 (alternating col5 stack) -> column-stack patterns matter.
- Steer (zero/max) on 6 positions: changes <= 0.02 in any column -> no measurable effect.

## Hypotheses
H1: center column low (1-2 stones) and opponent did not just play there.
H2: H1 + strongest when col3 = their stone at bottom, mine on top.
H3: mixture / dense layer-2 feature; may not have a clean rule.

## Score log
- s1 p1 (h3 in {1,2}, last_col != 3): F1 0.188 (P 0.109, R 0.693), AUROC 0.758, sim share 0.04.
- s2 p2 (+ top of col3 mine): F1 0.213 (P 0.137 R 0.474), AUROC 0.691, sim 0.05.
- s3 p3 (+ last stone landed in row 2-3): F1 0.201, AUROC 0.632, sim 0.04. Row heatmap of last move: band 9 has (3,5) and (0,0) at 22% each,
  (0,0) almost all being the ply-4 opening x,3,3,0 (an opening artifact).
- Cell occupancy by band: band 9 has (0,3)=theirs 72%, (1,3)=mine 68%, (1,5)=theirs 62%, (0,0)=theirs 61%, (2,2)=theirs 45%; col3 rows >= 2 ~never filled.
- s4 p4 (cell points: col3 low required; +2 their (0,3), +2 my (1,3), +1 their stone at each of (1,5),(0,0),(2,2),(2,4),(3,5),(2,1); -2 last move col3; fire at >= 5):
  F1 0.271 (P 0.227 R 0.335), AUROC 0.650, sim 0.08.
- Ply-4 scans (prefixes 3,3 / 3,2 / 2,3 x all 49 continuations): 2,3,3,y fires for all y != 3 (col3 = their,mine); 3,3,x,y (col3 mine,theirs) mostly
  does not fire; their stone at (0,2) strongly negative (3,3,3,2 = -1.9). Ply 4-7 is ~33% of firing vs 13% base.
- s5 p5 (p4 + ply terms, (0,6) mine, (0,2) theirs negative): F1 0.272 (P 0.265 R 0.279), AUROC 0.627, sim 0.08. No real gain.
- s6 p6 (simple: col3 exactly their+mine, last move not col3, ply <= 21): F1 0.225 (P 0.256 R 0.200), sim 0.09.

## Conclusion
Plateau at F1 ~0.27. Consistent core: low centre column (1-2 stones), ideally their stone at the bottom with mine on top,
and the opponent's last move not in the centre. Beyond that, the activation depends on many scattered cells with
interactions (minimal-pair grids are not additive). Looks like a mixture / dense feature -> confidence low.
Steer: zero or max changes every column probability by <= 0.02 on 6 positions -> no measurable effect.
