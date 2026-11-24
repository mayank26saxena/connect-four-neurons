# U44 notebook (layer 5, pole +, thr 0.491, rate 3%)

## Observations
- Top examples: opponent (O) stones in a horizontal row above row 0, often pairs like O(r,2),O(r,3) or O(r,3)..O(r,6) with floating empties.
- Minimal pairs: 3,3,4,4 fires 1.05 (O pair on row 1 above my stones); 0,3,0,4 (O pair row 0) -0.07.
  3,3,6,6 fires 0.91 but 6,6,3,3 (same board) 0.31 -> last move matters.
  56987 (3,2,6,3,3,6)=2.98; changing last move to any other column kills it (<0.65).
- steer: tiny effects (<0.07 prob).

## Hypotheses
H1: last move by O lies in a horizontal 4-window (row>=1) with >=2 O and no X.
H2: generic open horizontal O two/three above row 0 (not tied to last move).
H3: something about the model's col-2 preference (many top examples predict col 2).

## Tests and scores
- score h1 (last O stone in a no-X horizontal window with >=2 O): F1 0.058, AUROC 0.51. Dropped.
- Minimal pairs show strong conjunctive/order effects: board 143316 (3.33) needs O(0,1),O(0,4),XX(0,2-3),OO(1,2-3),X(2,2); removing any piece -> <0.4.
  3,3,4,4 fires (1.05) but 2,2,3,3 does not (0.08); 3,3,6,6 = 0.91 vs 6,6,3,3 (same board) = 0.31.
- score h2 (any horizontal open two, either colour, row>=1): F1 0.062, AUROC 0.52.
- Counts over examples: top band has cols 2-3 taller than cols 1 and 4 (51% vs ~7% in low bands) and same-colour pairs at cols 2-3 with 1,4 empty.
- score h3 (2-3 tower + pair): F1 0.082, AUROC 0.536.
- Counts: immediate win / must-block in column 4: band9 31%, b8 20%, b7 15%, b5-6 9%, bands 0-4 0-4%.
- score h4 (playable win or must-block in col 4): F1 0.118 (P 0.127, R 0.111), AUROC 0.544, sim share 0.03.
- score h5 (h4 OR tall 2-3 tower with pairs): F1 0.119, AUROC 0.561, sim 0.03.
- steer: effects tiny (<=0.12 prob); with --to max tends to raise cols 1 and 4 a few points, lower cols 3, 6, 0.
- synth: extending game 35098 (centre block in cols 2-4, many of my threat cells in cols 1/4/5) reached 8.96 (> dev max 6.0).

## Conclusion
No clean concept; very conjunctive and order-dependent; best F1 0.12. Possibly a random direction or mixture. Confidence low.
