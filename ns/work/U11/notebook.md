# U11 notebook (layer 5, pole -, threshold 0.519, dev max 19.5)

## Examples (40 + 25 extra)
- Bands 7-9 (act > 3): nearly all have the opponent's last move in column 6 completing a vertical three in col 6, cell above empty (must-block at (h,6)).
- Band 6: mixed; some vertical threes in other columns (pos 929 col 2, 2.4), some col-6 shapes, some unclear.
- Band 5: heterogeneous, no obvious pattern.

## Hypotheses
- H1: opponent has a vertical three on top of column 6 with the cell above empty (must-block in col 6 by vertical).
- H2: any opponent vertical three with open top (weaker in other columns).
- H3: any must-block in column 6 (horizontal/diagonal too).

## Minimal pairs (act)
- 6,1,6,2,6 (opp vertical 3 col 6): 5.97. Same in cols 0-5: 0.15, 0.07, -1.10, 0.00, -0.01, 0.19 -> column-6 specific (H2 rejected as main story).
- 6,0,6,0,6 : 10.1; 6,0,6 (only two): 0.05 -> needs three.
- After I block (6,1,6,2,6,6): -0.28 -> needs the top cell empty / threat live.
- My own vertical three in col 6 (6,0,6,1,6,2): -0.20 -> must be opponent's.
- Horizontal opp 3,4,5 with open (0,6): 0.33 -> H3 rejected.
- Opp three at rows 2-4 of col 6 on top of my two: 3.2-3.2 -> works at any height.
- Opp vertical three in col 0 with my 2 stones in col 6 (0,6,0,6,0): 1.43 (weak firing): other-column verticals give smaller activation.

## Dev metric
- score 1 (h1.py, col-6 opp vertical three, level 8 / other-col 2): F1 0.415 (P 0.928, R 0.267), AUROC 0.633, sim share -0.18.
- score 2 (h2.py, any column opp vertical three): F1 0.246 (P 0.195, R 0.331). Other columns add little recall at big precision cost -> col 6 specific.
- score 3 (h3.py, h1 + level graded by height 3/4/5 -> 9/7/4): same F1, sim -0.17.
- score 4 (h4.py, opp 2+ stacked on top of col 6): F1 0.234 (P 0.168, R 0.385). Rejected.
- score 5 (h5.py, h1 fires as graded number: 1.0 col-6 three, 0.3 other-col three, 0.2 col-6 two-stack; binary level): F1 0.415, AUROC 0.683, sim -0.17. FINAL.

## Remaining firing (~73% of firing positions, mostly act 0.5-3)
- Band 5-6 is diffuse: enriched for opponent two-stack on col 6 (21% vs 2%), col 6 height 1-3, vertical threes in other columns (e.g. pos 929 col 2 = 2.4, col 4 cases ~0.6), more threats overall; no single rule found.
- FPs of the col-6 rule are mostly threats in the top row (col 6 height 5) late in the game.
- Activation larger when the threat cell is low (h=3 ~10-19, h=5 ~1-6); persists (weaker) if the last move was elsewhere.

## Steer
- 3,2,1,1,6 (quiet): max -> col 6 +0.39 (from 0.00), col 2 -0.26. Forced must-block positions: already 1.00 on col 6, no change. Zero-ablation: no visible change on 6,1,6,2,6 and 15-ply example (col 6 stays 1.00, redundant).
- Effect: pushes the model to play column 6 (block the vertical threat).

## Synthesis (hill-climb with ns/work/U11/search.py over act)
- 6,0,0,0,2,0,3,1,0,2,3,4,5,5,4,4,6,4,2,2,6 -> 19.502 (dev max 19.528, just below)
- 6,0,2,0,0,2,3,4,4,1,3,4,6,0,2,3,6 -> 19.461; 6,0,0,0,2,0,3,1,0,2,3,4,4,4,6,4,2,2,6 -> 19.27

## Synthesis fix (orchestrator audit, after submission)
- 6,0,0,0,2,0,3,1,0,2,3,4,4,4,6,4,2,3,6 completes a four at move 18 (game over), so it is not a legal game. My search only checked column capacity.
- Checked all 5 with ns/work/U11/check4.py (it replays the game and finds the first completed four): only that one was bad.
- Replaced it with 6,0,2,0,0,2,3,4,4,1,3,4,6,0,2,2,6: no four, synth 18.685. Only `synthesis` and `notes` in final.json changed; resubmitted. No score calls used.
