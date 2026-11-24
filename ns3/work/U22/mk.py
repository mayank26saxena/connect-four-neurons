import json, sys
prog = open('ns3/work/U22/p1.py').read()
synth = [list(map(int, s.split(','))) for s in sys.argv[1:]]
d = {
 "unit": "U22",
 "description": "No clean concept found. Fires mostly in quiet positions (no immediate win or must-block) whose column heights avoid certain values: no column 0-5 with exactly 5 stones, column 6 with 0, 1, 5 or 6 stones, centre column with an even count. Within that, it depends on specific stones (e.g. early game: opponent holding the two bottom centre cells) and is not mirror-symmetric; one stone change often switches it on or off.",
 "effect": "Small: when forced high it raises column 6 by about 3-20 points, mostly taken from columns 4, 2 or 1; zeroing it on top positions lowers column 6 by 4-14 points.",
 "program": prog,
 "synthesis": synth,
 "confidence": "low",
 "notes": "Tried: H1 column-height allowed sets (p1, best: F1 0.146, AUROC 0.645, sim share 0.11); opponent vertical pair at a column top + heights (F1 0.125); strongest height dislikes + quiet, graded (F1 0.129, AUROC 0.696); opponent on (0,3),(1,3) (F1 0.097). Minimal pairs show cell-specific additive-looking contributions, mirror asymmetry and high sensitivity to the last stone: looks polysemantic or a random direction. Synthesis by act hill-climbing."
}
json.dump(d, open('ns3/work/U22/final.json', 'w'), indent=1)
print('written', len(d['description'].split()), 'words')
