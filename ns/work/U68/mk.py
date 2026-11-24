import json
prog = open("ns/work/U68/p4.py").read()
d = {
 "unit": "U68",
 "description": "Strongest when the opponent has three stones stacked on top of column 0 (also column 2, sometimes 4) with the cell above empty, so I must block there; stronger when I have stones in the centre (cols 3-4) of the bottom row. Same threats in columns 1, 3, 5, 6, and horizontal threats, do not fire. Most weaker firing (near threshold) is in quiet positions with no clear pattern.",
 "effect": "Weak. In forced (must-block) positions none measurable; in quiet positions forcing it high shifts about 2-9 points toward column 2 (sometimes 1) and away from column 5 or 3.",
 "program": prog,
 "synthesis": [],
 "confidence": "low",
 "notes": "Best dev F1 0.243 (P .28 R .21, AUROC .60), sim share 0.01. Top end (bands 8-9) is clearly opponent vertical threats in column 0/2 (act minimal pairs confirm column asymmetry: col 0 and 2 fire, mirror col 6 and cols 1,3,5 do not); but about 2/3 of firing is diffuse quiet positions that no tested rule captured (any must-block F1 .18; plus poisoned col 4 F1 .13; first-player-only col 4 F1 .23). Looks like a mixture or random direction with a structured tail."
}
json.dump(d, open("ns/work/U68/final.json","w"), indent=1)
