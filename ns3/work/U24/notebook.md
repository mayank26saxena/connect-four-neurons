# U24 lab notebook (layer 5, pole -, threshold 0.758, dev max 11.377)

## Observations (examples, 60/band seed 3 + default 40)
- Firing spans all game stages (mean ply ~19-21 in bands 8-9, same as band 0). No ply parity effect.
- Activations swing wildly (-11.7..+8.2) under single-stone substitutions in a top example (4,1,2,2,3,5,1,5,3): every stone matters -> distributed.
- Single-cell histograms band 9 vs band 0: me at (0,3) .73 vs .50, me at (1,3) .62 vs .25, them at (2,3) .62 vs .27; col 3 height>=3 in 57/60; col 0 empty 30/60 (vs 17), col 6 height<=1 47/60 (vs 24). Them at (4,2) 0/60.
- Last move col 3 in 21/60 top examples (vs 6/60 band 0).
- Threat-cell presence, forced-move structure (teacher scores), must-blocks: no separation.
- steer: tiny effects (<=0.1); forcing to max sharpens the model's existing top choice by 5-10 points; zeroing at top examples changes ~0-5 pts.

## Hypotheses
H1: centre-column stack: (0,3),(1,3) mine with their stone(s) above, col 3 height>=3.
H2: board shape: tall centre, empty edge columns. act tests (3,3,3,4,4,4,2,2,3 etc.) do NOT fire -> rejected.
H3: forced single good move / model confidence: teacher scores show no separation -> rejected.
Early-game minimal pairs (1,5,3,2,1 = 2.10): needs me at (0,2) and (0,5), them at (0,3),(0,1); (0,0),(0,4) must stay empty; adding them at (0,4) or (0,0) kills (-0.05). Conjunction of many cells; no simple tactical meaning found.

## Score calls
1. p1 centre stack (0,3),(1,3) mine + (2,3) theirs: F1 0.098 (P 0.064, R 0.208), AUROC 0.557, sim share 0.35.
   Misses often late-game with a nearly empty column among tall ones ("pit") -> tested with act: filling the pit sometimes raises, sometimes kills -> rejected.
2. p2 last move col 3 + edge columns low: F1 0.085, AUROC 0.536, sim 0.35.
3. p3 opponent just made a vertical pair in cols 2-4: F1 0.074, AUROC 0.534, sim 0.33.
4. p4 hand-weighted centre-column cues (sum>=8): F1 0.108 (P 0.106, R 0.109), AUROC 0.540, sim 0.33.
5. p5 crossed 2x2 square in cols 3-4 (from synthesis minimal pairs): F1 0.075, AUROC 0.540, sim 0.34.

## Minimal-pair findings
- Strongest synthetic: 5,4,3,1,2,4,3,3,4,3,4,4 = 12.76 (dev max 11.38). Crucial stones: col 3 me,me,them,them; col 4 them,them,me,me,them.
  The bare "brick" 3,4,3,4,4,3,4,3 does not fire (-0.96); adding a their stone on top of col 4 (or col 3) plus one extra stone of mine fires 3-11.5; my stone on col 4 instead kills.
- Left-right MIRROR of the 12.76 position gives -0.24: the unit is not mirror-symmetric, so it is not a game concept a player would recognise.
- Single-stone substitutions anywhere swing the activation by +-10: very distributed.

## Conclusion
No single board pattern found; all probes AUROC ~0.54. Likely a random direction or a heavily polysemantic unit. Confidence low.
Submitting the simplest probe (p1). Effect: steering to max sharpens the model's existing top move by ~5-10 points; zeroing changes <=5 points.
