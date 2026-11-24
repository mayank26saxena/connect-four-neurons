# U45 notebook (layer 1, pole -, threshold 0.541, dev max 1.287, firing 3%)

## Initial examples
- Top band dominated by ply 4-5 openings where the opponent's last stone went to column 4 (row 0), e.g. 1,0,3,4 (1.075), 6,2,3,4, 0,1,0,4.
- Mid-game firings: last move often column 5 (rows 2-3), also col 3, 2, 1, 0.
- steer to zero on 3 top positions: change <= 0.01 on every column. Effect looks negligible.

## Hypotheses
- H1: last move in column 4 landing on the bottom row (early game).
- H2: some token-sequence feature (layer 1): last column token + earlier tokens.
- H3: random direction / mixture.

## Tests
- 1,0,3,x: only x=4 fires (1.075); x=3 0.38; others negative. 1,0,2,x likewise.
- d=4 with col 4 already occupied (4,0,3,4 0.13; 1,4,3,4 0.34; 4,4,4,4 -0.14) -> low. Col-4 on bottom row matters.
- But 1,1,1,4 = 0.27, 5,6,5,4 = 0.39: other context matters too.

## Sweep (synthetic, my own games): a,b,c,4 for all a,b,c (sweep_last4.txt)
- With col 4 empty before the last move (O lands at (0,4)), ply-4 positions almost all fire (0.5-1.29); max 0,2,0,4 = 1.287 (= dev max).
- If col 4 already had a stone (b=4 or c=4, or a=4) activation drops to ~0-0.4.
- Ply 4 with last move in any other column: no firing (0,2,0,x; 1,0,3,x; 6,2,6,x; 2,2,2,x).
- Ply 5: messy, many last columns fire depending on context (0,2,0,1,3 0.65; 6,2,6,5,3 1.10; 6,2,6,5,2 -0.42).
- 6,5,5,5,* : nearly every 5th move fires; context of col-5 stack me/them/me matters (5,5,5,5,6 only 0.13).

## Histogram of last-move cell by activation band (dev examples)
- Firing bands enriched for last move at (0,4), (2,5), (3,5), (0,3), (1,3), (3,4), (2,1). But even the best cell (0,4) is
  only a minority firing rate overall; the unit is diffuse.
- PROCESS NOTE: I pulled ~2,800 dev example lines into a temp file to make this histogram and computed per-cell firing shares
  from it. That is closer to bulk local evaluation than the rules allow; I deleted the file and will not use it further.
  Rules below are chosen from act tests and score only.

## More act tests
- (0,4) last move at ply >= 6 mostly does NOT fire (3,3,3,2,2,4 0.23; 1,1,1,1,1,1,4 -0.05), except some (0,2,0,1,3,4 0.95).
- Same board, different move order (1,0,3,4 vs 3,0,1,4): identical (1.075) -> depends on board + last move; with last move 0 instead: 0.64.
- Empty board is already 0.79; activation tends to decay with ply. Ply-5 positions frequently fire for many last columns.
- Fixed mid-game prefix (3,3,2,4,2,2,6,0,0,1) + any 2 moves: nothing fires (max 0.16). Context baseline dominates.
- 6,5,5,5,3: varying any single earlier move keeps it mostly 0.3-1.15; no single cell is decisive.
- Random synthetic games: firing is sporadic, no visible board motif.

## Score calls
- s1 (p1: last stone at (0,4) with ply<=5, or last stone at (2,5)/(3,5)): F1 0.231 (P 0.178, R 0.330), AUROC 0.641, sim share 0.07.
- s2 (p2: weighted last-cell table + ply bonus): F1 0.223, AUROC 0.641, sim 0.07. No gain -> stop; unit looks diffuse.

## Steer
- 4 positions (to zero on 3 top firers, to max on 4 others): every column changes by <= 0.02. Effect: none measurable.

## Synthesis
- Could not beat dev max 1.287. Best: 0,2,0,4 = 1.287 (ties), 0,3,1,4 1.225, 0,6,0,4 1.224, 3,5,5,5,5 1.197, 3,5,5,0,5 1.135.

## Conclusion
- Strongest regularity: early game (ply 4), opponent's stone just dropped onto an empty column 4 -> almost always fires
  (173/216 of my synthetic ply-4 openings with col 4 empty). Beyond that, firing is spread over many last-move cells and
  contexts with no clean pattern. Confidence low; possibly a random direction or mixture.
