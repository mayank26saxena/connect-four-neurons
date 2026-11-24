# U54 notebook (layer 3, pole +, threshold 1.186, dev max 3.047)

## Observations from examples (~60 viewed, plus single-feature histograms of 800 sampled positions)
- Top band (>2.0): very often column 4 is empty or has 1 stone while columns 3 and/or 5 are tall (a "well" at col 4).
  Several mid-game tops have an opponent threat at (2,4) right above my col-4 landing (col 4 poisoned), but removing the threat
  (minimal pair 5,4,3,5,3,3,5,3,6,1,5) keeps it firing (2.53), so the threat is not required.
- Many early (ply 5-9) firing positions have no well; activation depends on scattered stones (e.g. O on (0,0) raises, O on (0,4) lowers).
- Cell histograms (act>1.7 vs <0.5): (1,4) empty 91% vs 71%; col4 height<=1 in 69% of >1.7 vs 35% of <0.5.
- steer to max / zero: changes move probs by <=0.01 on 3 positions -> no measurable effect.

## Hypotheses
H1: col 4 is low (<=1 stone) while a neighbour (col 3 or 5) has >=3 stones.
H2: col 4 low at all (<=1) (broader).
H3: diffuse / mixture; possibly a random direction.

## Minimal pairs
- 5,4,3,5,3,3,5,3,2,1,x: x=5 3.05, x=4 (col4 h->2) 1.10, x=6 0.39, x=0 -0.28. Last move strongly matters, not just col-4 well.
- 0,3,3,6,6 = 2.10; changing first move 0->4 (O at (0,4)) = 0.00; 0->1 1.29; 0->5 0.41.
- 1,3,3,1,x: x=6 2.13, x=4 -0.47.
- 4,4,4,3,x: x=0 2.23, x=5 0.44.

## Score 1 (p1: h4<=1 and max(h3,h5)>=3): F1 0.088, P 0.049, R 0.39, AUROC 0.585, sim share -0.01. Well alone is far too broad
(FP e.g. late boards with empty col 4 surrounded by tall columns, act ~0).

## More tests
- Ply-controlled (ply 8-18) cell histograms, act>1.6 vs <0.7: (0,5) theirs 53 vs 39%, (2,5) theirs 26 vs 5%, (1,4) empty 60 vs 43%,
  (2,4) mine 6 vs 21%. Top-of-column-5 is theirs 61% (act>1.7) vs 45% (act<0.5); other columns ~flat.
- Minimal pairs on 5,3,3,5,5,4,0 (2.36): +0,5 (O on top of col 5) 2.19 vs +5,0 (X on top of col 5) 0.47; +4,4 1.86; +1,1 0.79; +2,0 0.38.
- Same final position reached by different move orders gives 1.86 vs 2.36: some sequence dependence.
- Ply parity, last-move column, stone under last move: no clear differences across bands.
H4: col 5 topped by an opponent stone, col 4 lower than col 5.

## Score 2 (p2: col5 topped by theirs, h4<=1, h5>h4): F1 0.101, P 0.062, R 0.28, AUROC 0.578, sim -0.02.
Misses show the same motif on other columns (e.g. col 3 topped by O beside a low col 4, col 3 gap). Band-7 samples: many have
opponent-topped columns flanking a low "hole" column (mostly col 4, sometimes col 3 or 1). But dev FPs include boards with this
shape and act ~0, so it is at best a weak tendency.
H5 (generalised): an opponent stone tops a column that stands >=2 higher than a horizontally adjacent column (a hole beside an O-topped tower), counted over columns 2-5.

## Score 3 (p3: >=2 opponent-topped towers next to a hole in cols 2-4): F1 0.060, AUROC 0.522, sim -0.02. Worse; abandoned.

## Steering (6 positions incl. 3 firing at 2.1-3.4): forcing to max or zero changes every column's probability by <=0.02. No measurable effect.

## Synthesis
4,5,3,5,3,3,5,3,2,1,5 = 3.361 (beats dev max 3.047). Same shape as the dev top position 48590 with the first two moves swapped.
Others 2.57-3.05 (below max).

## Conclusion
No rule above F1 0.11 / AUROC 0.59 after 3 genuinely different hypotheses. Activation depends on scattered stones and the move order
(the same board via two orders gave 1.86 vs 2.36), and steering does nothing. Looks diffuse, maybe a random direction. I stopped at 3 of 8
score calls because the remaining ideas would only be overfit tweaks. Submitting p2 (best F1) with confidence low.
