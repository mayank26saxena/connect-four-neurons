import json
prog = open('ns/work/U03/p4.py').read()
d = {
 "unit": "U03",
 "description": "No clean concept found. The strongest activations are sparse early-game positions (about 4-10 stones) with the centre column still empty, especially when my bottom-row stones are close to a horizontal three or four through column 3 or 4 (e.g. X.XX on the bottom with column 3 open). Most firing elsewhere is spread over varied mid-game positions that no simple board rule captures.",
 "effect": "None measurable: forcing it high or off changes move probabilities by at most about 0.06.",
 "program": prog,
 "synthesis": [[5,5,2,5,4,0],[5,5,2,5,3,0],[5,5,2,5,1,1],[5,5,2,5,4,0,6,4],[5,1,2,1]],
 "confidence": "low",
 "notes": "Hypotheses: bottom-row open two (F1~0.15 local), early+col3 empty (dev F1 0.213), col3 threat cells (weak), bottom-row immediate win (precise but 3% recall). Best dev: F1 0.226, AUROC 0.65, sim share 0.02. A boosted classifier over board features reaches only ~0.25 CV F1, so the unit may be a random direction or mixture. Synthesis 5,5,2,5,4,0 reaches 15.9 vs dev max 12.2."
}
json.dump(d, open('ns/work/U03/final.json','w'), indent=1)
