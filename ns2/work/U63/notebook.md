# U63 notebook (layer 2, pole -, threshold 0.679, dev max 2.096)

## Observations
- Firing is concentrated in the early game (ply 4-12); band 0 contains all plies.
- Top: 3,4,2,5,2,2 (2.06), 0,3,1,4,1,5 (1.88), 0,5,3,0 (1.51), 3,3,0,0, 6,1,0,0, 1,5,2,5,0,0.
- Move-order invariance roughly holds (2,4,2,5,3,2 = 2.08).
- Strongly left-right ASYMMETRIC: mirrored versions of top positions are mostly off (-0.9..0.8).
- Opponent stone stacked on my (0,0) in 4-stone positions fires for nearly all placements of the other two stones.
- But 0,3,0,0 (X X O stack in col 0) = -1.25.
- Steer effect tiny (<= 5 points).

## Hypotheses
H1: early game + my stone(s) in the left bottom (col 0-1) with their stone above.
H2: early game + opponent stones on the right half of bottom row (theirs (0,4) is 60% in band 9).
H3: generic "few stones" with a left-side bias (possibly random-direction-like).

## Tests
- Swept all 2,401 four-move openings with act (ns2/work/U63/all4.txt): 189 fire. Per-cell mean activations are small and mixed:
  theirs (1,0) +0.61, mine (0,0)/(0,1) ~+0.25, theirs (0,6) -0.45, theirs (0,2) -0.26. No clean concept.
- The col-0 stack (their stone on my (0,0)) fires in most 4-stone positions but NOT later in the game (3,3,4,4,2,5,0,0 = -0.26).
- Within a single game the activation swings by 0.5-1.0 from one move to the next and tends to be higher at even ply (me = first player).
- Mid-game firers: no distinctive empty-column count, under-stone owner, or "answered on top of my last move" signal (histograms flat).
- The opponent's last move into the right side (cols 3-5) raises it a little in two minimal-pair families.

## Dev metric
- s1 p1 (ply<=10 and me_first): F1 0.147, P 0.09, R 0.40, AUROC 0.64, sim -0.01
- s2 p2 (ply<=12 + their stone on my (0,0)): F1 0.124, P 0.18, R 0.095, sim +0.04
- s3 p3 (hand-weighted cell score + early + parity): F1 0.172, P 0.145, R 0.21, sim -0.04
Stopped scoring: each rule only nudges F1, which points to a distributed or random direction rather than a missed concept.

## Steer
5 positions, to max or zero: changes of 5 points or less (mostly under 1). Effect is negligible.

## Synthesis
Best found: 0,0,1,0,5,5 (2.085), 0,4,1,0,5,5 (2.084), 2,4,2,5,3,2 (2.080), 1,4,0,0,5,5 (2.076), 0,3,1,4,1,5,4,4 (2.051), all just under the dev max 2.096.

## Conclusion
Low confidence. It is mostly an early-game unit with a left-side bias, and the activation is very noisy from move to move. Possibly a random direction.
