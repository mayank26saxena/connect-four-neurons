# U84 notebook (layer 3, pole -)

## Observations
- Band 9 cell histograms: me at (1,1) 74%, me at (2,2) 80%, them at (1,2) 60%, (2,1) 53%, (0,3) them 63%; col 0 height <=2 in 100% of band 9; col1 height 2-4.
- Strongly left-side specific: mirrored positions do not fire; motif shifted one column right/left does not fire.

## Hypotheses
H1: checker motif in cols 1-2: me (1,1),(2,2), them (1,2) [+ (2,1)], with their anti-diagonal (0,3)-(1,2)-(2,1) aiming at (3,0) and col 0 low.
H2: their stones forming lines toward column 0 (e.g. row-0 three 1,2,3 with (0,0) open fires 1.2).
H3: col 0 low / col 1 medium staircase (heights) - too unspecific alone.

## Minimal pairs (act)
- 1,2,1,2,2,1 (pure motif) 1.67; colours swapped -0.33; motif shifted right 0.16-0.26.
- + their (0,3): 5.04. Remove (2,2): 2.0; remove (2,1): 2.6; remove (0,3): 1.6; (1,1) empty: 0.18; (1,1) theirs: ~-0.8.
- my (0,4) raises (5.07); my stone at (0,0) lowers; their stone in col 0 lowers in 7.0 position.
- 147758 variant: their stone at (1,3) or (1,4) kills it (0.29 / -0.05): unexplained exception.

## Score log
- s1 p1 (checker motif me(1,1),me(2,2),them(1,2) + bonuses): F1 0.153, AUROC 0.584, sim share 0.04. Motif is a common opening shape; most motif boards do not fire (col 0 usually tall in FPs).
- s2 p2 (motif + col0 h<=1): F1 0.190, sim 0.03.
- s3 p3 (skyline: h0<=1, h1 in 2-3, h3 not 3-4, h4 not 2-3, + motif cells): F1 0.255, AUROC 0.606, sim 0.09.
- s4 p4 (their anti-diagonal (0,3)-(1,2)-(2,1)-(3,0) open, col0 low): F1 0.146.
- s5 p5 (cell-weight composite incl. row-0 them(0,2)/me(0,4)): F1 0.207.
- s6 p6 (p3 + h0==0, h6<=1 bonuses): F1 0.257 (P 0.21 R 0.33), AUROC 0.643, sim share 0.07. BEST.
- s7 p7 (p6 + centre-well h2,h4 >= h3+2): F1 0.238. No gain; stopped.

## Other findings
- Early-game firing (4-7 stones) has a second family: their stones at (0,2) (+(0,1)) with my stone at (0,4) and (0,3) empty (4,2,6,1 = 1.59; their (0,3) instead kills, my (0,3) instead kills).
- Board-based (same board via other move orders: 5.7-7.0), colour-specific, left-side specific (mirror does not fire).
- Filling column 0 kills firing; filling col 3 to height 3 kills it.
- Steer: tiny effects (<= 0.1 prob), mostly lowers column 3 and raises col 1/0/2 by a few points.
- Synthesis: 2,1,2,2,0,1,2,4,3,2,1,5,5,4,4,4,4,6,5 reaches 12.15 (dev max 7.43): skyline [1,3,5,1,5,3,1], centre well.
- Conclusion: no clean single concept found; looks like a distributed left-side/skyline feature or mixture. Confidence low.
