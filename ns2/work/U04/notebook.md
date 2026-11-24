# U04 notebook (layer 2, pole -, threshold 0.830, dev max 2.093, firing 3%)

## Observations
- 40+ examples across bands: firing skews early game (ply 4-8 ~60% of firing), more empty columns.
- Top examples: 0,0,6,6 (1.76), 6,6,0,0 (1.81); several with their vertical three (must-block above) e.g. 137874 (1.99), 83217 (1.81).
- Activation swings wildly ply-to-ply within a game (e.g. +1.56 -> -0.03 -> +1.99).
- Single-feature histograms (top owner per column, last-move row, below-last, neighbors): only weak shifts. Last move horizontally isolated (empty left/right) more common in firing (~60% vs 40-50%).
- Minimal pairs from 0,0,6,6: changing any one move shifts act 0.2-1.8 with no clean rule (0,0,6,4 1.20; 0,0,6,1 0.20; 2,0,6,6 0.23; 1,0,6,6 1.03).
- Their vertical three on its own (0,3,0,3,1,3) does NOT fire (0.01).
- steer --to max on 3 non-firing positions: changes <= 0.03 probability. --to zero on top position: <= 0.01.

## Hypotheses
H1: early sparse board + last move horizontally isolated.
H2: random direction / mixture (no clean concept).

## Scores
- p1 (H1: ply<=10 and last move horizontally isolated): F1 0.108 (P 0.067 R 0.282) AUROC 0.579, sim share -0.16. (first run crashed on last_col None; fixed guard.)
- p2 (>=3 empty columns): F1 0.111 AUROC 0.607, sim -0.06.
- p3 (additive sparse-board score: ply, empty cols 1/2/4, isolated last move): F1 0.139 (P 0.099 R 0.231) AUROC 0.582, sim -0.15.
- p4 (same fires, level 0 unless fires): F1 0.139, sim -0.15.
- H4 from act: "capped pairs" (my stone with their stone directly on top, in columns of height 2) on an otherwise empty board, edge columns 0/6 strongest, col 2 suppresses:
  0,0,6,6 1.76; 6,6,5,5,0,0,3,3 2.13; 5,5,6,6,3,3,0,0 2.24 (beats dev max). But 2,2,4,4 0.40, 6,6,5,5 0.45; same board in different move order differs (0,0,3,3 0.55 vs 3,3,0,0 1.00) -> not purely a board function.
- p5 (capped-pair weighted count >=3): F1 0.050 (P 0.075), AUROC 0.51. Pattern does not generalize to dev (in fuller boards it never fires).
- p6 (sparse-board score + capped-pair bonus, ply<=10 only): F1 0.144 (P 0.174 R 0.122) AUROC 0.552, sim -0.07. Best.

## Effect (steer)
- to zero on 3 firing positions (0,0,6,6; 2,1,1,6,1,1,2,2,4,2,0,2; 6,4,5,0,3,3,3,4,3,5,6,6,3): change <= 0.01.
- to max on 3 non-firing positions: change <= 0.03. No measurable effect.

## Conclusion
No clean concept. Firing is weakly enriched for early, sparse boards; activation swings strongly ply-to-ply and depends on move order.
Looks like a random direction or a diffuse mixture. Confidence low.
