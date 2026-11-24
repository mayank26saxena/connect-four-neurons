# U19 notebook (layer 2, pole +, thr 1.273, dev max 6.03)

## Examples (ex1.txt, band 9 seed1)
- Almost every firing example: top stone of column 4 is THEIRS (O) and sits directly on MY stone (X).
  Often col 4 full with col 3 full too (highest acts). Last move often in col 4.
- Counter: 47151 has O-over-X top of col4 (h=2) but act -0.02; 4,4,4,4,4,4 has it but -0.06.

## Hypotheses
H1: top of col 4 = O directly on X.
H2: H1 plus central columns (3) filled / many stones -> higher.
H3: last move by them into col 4 on top of my stone.

## act tests
- base 0,5,1,...,2,4 (6.03): replacing last move (col4) with 0/2/5/6 -> 0.6-1.0.
- 4x6 alone -0.06; 3x6 then 4x6 -> 1.89; 0,1,0,4x6 -> 1.03.
- 3,4,0,2,4 -> 2.12 (O over X at h2); 4,3,0,2,4 (O over O) 1.29; 3,4,0,2,4,4 (X on top) 0.10.

## Scores
- p1 (top col4 = O on X, any height): F1 0.201 P0.11 R0.89
- p2 (h4 in {2,6}, O on X): F1 0.374 R0.89
- p3 (h4==6 top O, or h4==2 top O & ply<=8): F1 0.386 P0.24 R0.987, sim share 0.42
- p4 (p3 + decay with plies since col4 filled): F1 0.464 P0.36 R0.66, sim 0.55
- p5 (p4 + bonus per other full column): F1 0.405 - worse
## act findings
- Strong recency: 4.09 right after them filling col 4, ~2.3 two plies later, ~1.4 four, ~1.1 six.
- Top X in full col 4 -> ~0 (synthetic). Same board but O,O on top -> ~1.1-1.3 vs X,O -> 2.9.
- Heights 3-5 of col 4 with O-on-X: ~0. h=2 fires only early in game.
- After decay, them completing ANOTHER column (a new top-row stone) re-boosts (1.04 -> 2.0). Filling non-top no.
- Examples: (their top-row stones - my top-row stones) higher in fires than in FPs.
- p6 (top-row their-minus-mine count + recency): F1 0.433
- p7 (recency = since opponent's last top-row stone, longer window): F1 0.446, R0.83, sim 0.52
- p8 (p7 shorter window): F1 0.434
- FINAL = p4 (best F1 0.464, sim share 0.55).
## steer
- zero / max on 4 positions (6.03, 2.12, 2.61, 2.27): move probabilities change <= 0.05; effect negligible.
## synthesis
- base dev game variants: ...,2,1,2,0,0,4 -> 6.144 and ...,2,1,2,4 -> 6.077 (beat dev max 6.030); clean synthetic 0x6,5x4,4x6 -> 4.33.
