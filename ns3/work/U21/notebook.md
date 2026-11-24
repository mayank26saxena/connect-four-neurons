# U21 notebook (layer 0, pole +, thr 0.611, rate 3%, dev max 1.813)

## Observations from examples (~100 positions)
- Top band (>1.15): nearly all ply 4-6, last move (theirs) in col 2, col 3 empty.
- Bands 5-8: also last col 4 early, and late-game (ply 15-39) positions with last col 6 / 0 (often high in the column).
- Layer 0: behaves like a bag of move tokens: 4,6,6,2 == 6,6,4,2 (0.927 vs 0.928), order-insensitive.

## Minimal pairs (ply 4, last move 2, vary one earlier move from 6,6,6,2 = 0.386)
- my stone (plies 1/3) in col 4: +0.54; col1 +0.32; col0 +0.21; col3 -0.09; col5 -0.05; col2 (under) -0.36
- their stone (ply 2) col2 (stacked) +0.37, col1 +0.25, col4 +0.23, col0 +0.04, col3 -0.17
- 4,1,1,x: x=2 1.59, 4 0.52, 5 0.57, 0 0.37, 1 0.32, 3 0.16, 6 -0.21  -> last col 2 dominant
- Activation decays with ply (dilution): 3,3,3,3,3,2 = 0.42, 1,1,0,0,1,1,0,0,2 = 0.50

## Hypotheses
H1: last move in col 2 early in the game (ply <= ~8), col 3 empty-ish.
H2: H1 plus a late-game branch: last move col 6/0 landing high.
H3: unit is a token-mixture (layer-0 bag of moves) without a clean board concept.

## Score log
- s1 p1 (last=2, ply<=8, h3<=1): F1 0.249 (P .31 R .21), AUROC .60, sim share 0.04
- s2 p2 (scored mixture: last=2 + h3/my-col2/ply; last=6 high stack with cols1-2 not full; others low): F1 0.312 (P .37 R .27), AUROC .63, sim 0.08
- additive token model from 12-ply substitution pairs (p3) NOT scored: failed sanity check on hand sequences (predicted -0.46 vs act 0.89 for col-6 stack) -> unit is nonlinear in token mix.
- s4 p4 (ply-graded levels, last=6 by height): F1 0.262 (P .19 R .42), AUROC .68, sim 0.12. last=6 high-stack branch kills precision (common below threshold too).
- s5 p5 (last=2 + h3<=1 + no my stone in col2): F1 0.271 (P .53 R .18), sim 0.09
- s6 p6 strict core (last=2, h3==0, no mine in col2): F1 0.196 (P .55 R .12)
- s7 p7 = p2 detection with graded level: F1 0.312, AUROC .63, sim share 0.12  <- final

## Other findings
- Order-insensitive at layer 0 (bag of moves by player), strong context interactions (col-3 stones negative for almost every last column; col-6 stacking raises it when last move is 6).
- Firing spread over last columns: ~40% last=2 (mostly ply 4-6), ~20% last=6 (col 6 stacked to row>=3), rest last 0/1/3/4 with no clean board pattern found.
- steer max / zero on 5 positions: move probabilities change by <=0.04, typically 0.00-0.02 -> no measurable effect.
- Synthesis: 1,2,4,2 = 1.813 (= dev max), 4,2,1,2 1.810, 1,1,4,2,4,2 1.610.
- Conclusion: mixture / possibly random direction; low confidence.
