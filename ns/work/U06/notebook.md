# U06 notebook (layer 5, pole -, threshold 0.870, dev max 13.835)

## Examples (40 across bands + ~60 more in bands 5-6)
- Bands 7-9 (act > 2.6): nearly all have a must-block in COLUMN 0 (opponent's vertical three in col 0, last move col 0; also (4,0),(5,0)).
- Band 5-6 (0.87-2.6): diffuse. Must-blocks in other columns (col 5 vertical three ~1-2.5, col 2, col 6), plus many
  early-game positions with no tactics (e.g. 4,2 -> 0.94; 4,5 -> 1.29; 6,5,0,5 -> 2.1).

## Hypotheses
- H1: fires when the opponent threatens an immediate win at column 0 (must-block in col 0). Strength ~ highest.
- H2: any must-block, column 0 strongest, column 5/2 weaker.
- H3: residual early-game/no-tactic activity, maybe a weak bias toward ... (unclear).

## Minimal pairs (act)
- 3,0,4,0,3,0 (O vertical three col 0, must-block (3,0)): 8.22 FIRES; same before O's third stone (3,0,4,0,3): 0.02.
- Same vertical three in col 1: -0.32; col 2: 1.34; col 3: 0.13; col 4: -0.05; col 5: -1.7; col 6: -2.5.
- Horizontal O three 1,2,3 on bottom with block cell (0,0): 2.66 FIRES; mirrored (block (0,3)): -0.23.
- 1,0,0,0,3,0,6,0 (O three in col 0 rows 1-3, block (4,0)): 4.71.
- 1,0,2,0,3,0 (col0 must-block but I have my own immediate win): 2.49 (reduced from ~8).
=> H1 confirmed: the core is "must-block in column 0"; vertical strongest, horizontal weaker; own win reduces it.

## Score calls
- Call 1 (h1, accidentally printed only tail) and call 2 (h1 again): any must-block in column 0. F1 0.436 (P 0.611, R 0.340), AUROC 0.666, sim share -0.20.
  FPs: col-0 must-blocks that are diagonal, or late-game ones with other threats around.
- Call 3 (h2): + vertical opponent threes in col 2/5. F1 0.435 (P 0.452, R 0.418). Col 2/5 verticals are unreliable (many don't fire); dropped.
- Call 4 (h3): col-0 vertical/horizontal only, no other must-block. F1 0.416 (P 0.720, R 0.292). Horizontal at row>0 often doesn't fire.
- Call 5 (h4): h3 + early-opening cluster (I have two stacked in col 4, ply<=8). F1 0.412: early cluster too irregular (e.g. 4,5,4,6 2.96 but 4,2,4,6 0.61; 4,5,4,0 -3.7).
- Call 6 (h5): h1 detection with graded level (vertical 9 > horizontal 6 > diagonal 4, minus for extra threats/own win/late game). F1 0.436, sim share -0.04.

## Extra minimal pairs
- Diagonal-only col-0 threat (1,1,2,3,2,2,3,6,3,3, block (0,0)): 0.24, no fire.
- Horizontal bottom-row threat at (0,0): 2.66 in 4,1,4,2,6,3 but -0.30 in dev pos 59766 (me second player). Inconsistent.
- Col-0 threat persists after an unrelated pair of moves (3,0,4,0,3,0,6,5): 4.2 still fires.
- Residual ~2/3 of firing is in band 5-6 (0.87-2.6): diffuse, many early openings (4,5: 1.29; 4,5,4,2: 3.38; 4,1,4,2: 2.09), some col-5 vertical must-blocks. No simple rule found.

## Steering
- 3,4,2 to max: col 0 0.03 -> 0.12 (+9 pts). 3,3,2,4,4,4 to max: col 0 +8 pts. 6,5,0,5: col 0 +1 pt. 3,0,4,0,3,0 zeroed: no change (model already plays col 0 with p=1.00).
=> effect: pushes the move toward column 0, modestly; not needed for the block itself.

## Synthesis
Greedy extension of dev pos 148282: 4,1,3,5,5,3,1,5,5,1,0,5,6,5,0,2,4,6,6,4,0 -> 14.29 (beats dev max 13.84). Also 14.26, 13.94, 13.93.

## Conclusion
Top 1% of activation (>2.6) is almost exclusively "opponent threatens to win at column 0 (must-block in col 0), esp. a vertical three in col 0".
Lower firing band is diffuse. Best F1 0.436 -> confidence medium.
