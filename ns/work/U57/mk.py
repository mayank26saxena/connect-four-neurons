import json
prog = open('ns/work/U57/v1.py').read()
d = {
 "unit": "U57",
 "description": "Fires when the opponent has three stones stacked vertically at the top of column 1 (second column from the left) with the cell above empty, i.e. a vertical must-block in column 1; very strong (20-65), especially right after they played there. A vertical three in column 5 gives weak firing (about 1-2). Horizontal/diagonal threats in column 1, my own vertical threes, and other columns do not fire it. Much weak near-threshold firing is unexplained.",
 "effect": "Pushes the move to column 1 (blocking): forcing it high raised column 1 by +0.37 to +1.00 probability on three positions; zeroing it at real column-1 threats changes nothing (block chosen anyway).",
 "program": prog,
 "synthesis": [[1,5,3,3,1,2,5,4,3,3,6,6,1],[1,5,3,3,1,2,5,4,3,3,1],[1,5,3,3,1,2,6,4,3,3,1],[1,5,3,3,1,2,5,5,3,3,6,6,1],[1,5,3,3,1,2,5,5,3,3,1]],
 "confidence": "medium",
 "notes": "Col-1 vertical-three rule alone: F1 0.393 at precision 0.994, recall 0.245. Adding col-5 vertical three: F1 0.441 (P 0.666, R 0.329), AUROC 0.66. A ply<=22 cut on col 5 gave 0.446 (not adopted). Simulation share nan (ceiling negative). Minimal pairs confirm vertical-only, opponent-only, column-1 specific. Remaining ~70% of firings are a diffuse 0.7-3 tail with no clean concept. Three synthesis positions beat dev max (68.9)."
}
json.dump(d, open('ns/work/U57/final.json','w'), indent=1)
