# U42 notebook (layer 0, pole +, threshold 1.667)

## Observations
- Every firing example (bands 5-9) has last move in column 2 (opponent just played col 2).
- Top examples: column 2 has several of MY stones underneath and their stone just landed on top.
- Strong ply dependence: same col-2 pattern after 6 moves ~0.85, after 12 ~1.8, after 18 ~4.0.

## Hypotheses
H1: last_col==2 alone. Rejected: 2,2,2,2,2,2 and 3,2,3,2,... sequences stay < 0.6.
H2: last_col==2 AND my stones in column 2 (count matters), opponent's own earlier col-2 stones suppress, grows with ply.
H3: parity effect only (who played last). Folded into H2: col-2 stones by the same player as the last move suppress.

## Minimal pairs (act)
- prefix P(13 moves)+2,2 = 4.04; +5,2 / +3,2 / +6,2 / +0,2 ~3.5 (still my two col-2 stones below); +2,5,2 = 0.10 (now col-2 stones are theirs).
- neutral 12-move prefix + 2 (no col-2 stones) 0.04; +2,3,2 (their own below) 0.27; +2,3,3,2 (one mine below) 1.77; +2,4,2,4,2,2 (three mine) 3.98.
- 2,0,2,0,2,2 (three mine, ply 6) 0.84; same pattern at ply 12 1.82, ply 20 4.29.
- Rough rule: score = ply + 2*my_col2 - 3*their_col2_before, fires if >= 18.

## Dev metric
- call 1 (output truncated, same as call 2) / call 2 p1 (ply + 2*mine - 3*theirs >= 18): F1 0.670 (P .54 R .88), AUROC .929, sim share 0.97.
- call 3 p2 (mine 2.5, theirs 1.5, thr 19): F1 0.649, share 0.93. Misses at low ply with several of my col-2 stones; FPs with many of their col-2 stones.
- More act tests: ply effect is not monotone, peaks ~ply 18-20 then decays slowly (n=1: 18->3.3, 22->2.7, 26->2.1). Single "my col-2 stone" is worth ~+1.8 at ply 18 (mine=0: ~1.5). Other columns modulate +-0.4 (col 3 stones help, cols 1/5 by me hurt in that prefix): token-level layer-0 effect, not modelled.
- call 4 p3 (estimate in activation units, peaked ply curve, +0.9 per extra my stone, -0.5 per earlier their stone, requires mine>=1): F1 0.720 (P .594 R .917), AUROC .949, share 0.98.
- call 5 p4 (= p3 plus mine=0 case allowed with -1.0): F1 0.720, share 0.99. FINAL.
- call 6 p5 (thr 2.0, steeper decay, theirs 0.7): F1 0.701 (P .755 R .655). Overshot; keep p4.

## Steer
Zeroing at 4.0-5.3 activations: changes <= 7 points, inconsistent direction (e.g. +0.07 col 4 once, -0.06 col 4 another, +0.03 col 0). Max-steer on a weak position: -0.06 col 3, +0.05 col 4. Effect: essentially none measurable.

## Synthesis
Greedy single-move edits of top dev game 43121 (5.32): 7.29, 7.28, 7.26, 6.30 beat dev max 5.48.
