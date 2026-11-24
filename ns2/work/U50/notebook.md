# U50 notebook (layer 1, pole -)
## Observations
- Top bands dominated by last move in column 4 (band 9: 43/60 last col 4; band 0: 3/60).
- 3,1,6,4 = 1.34; changing last move to other cols drops to <0.5. Mid-game 82289: only last=4 (1.02) and last=6 (0.60) fire.
- Not mirror symmetric (col 2 mirror fails).
- Last col-4 stone placed on top of MY stone fails (3,1,6,4,4 -0.23; 3,1,6,4,2,p,4 all ~0); on floor or on THEIR stone fires (3,1,6,4,2,4 0.81).
## Hypotheses
H1: opponent's last move went into column 4, landing on the floor or on their own stone.
H2: simply last move col 4.
H3: their stone at (0,4) with (0,5) empty (some non-last-4 firing cases: 2,4,6,6; 6,4,2,3).

## Score log
- p1 (last col 4, on floor or on their stone): F1 0.142, P 0.104, R 0.225, AUROC 0.583, sim -0.01. Below-stone rule broken by mid-game cases (5503: O on X fires).
- Histograms: col 5 empty strongly enriched at top band (74/80 in band 9), but bands 5-6 (most firing) mostly have neither last=4 nor col5 empty. Mean ply falls with band (19 -> 7). No ply-parity effect.
- p2 (last 4 & col5 empty, or last 5 & col4 empty; graded level): F1 0.142, AUROC 0.584.
- p3 (weighted last col / col5 empty / early ply): F1 0.132, AUROC 0.55.
- p4 (col 5 empty gap between filled cols 4 and 6): F1 0.129.
- p5 (last col 4 and col 5 empty): F1 0.172, P 0.154, R 0.194, AUROC 0.581, sim -0.03. BEST.
- Late-game firing often has a near-empty column (3/4/5) in a crowded board, but not enriched in histograms vs non-firing.
- Mid-game trajectories flip firing on/off move to move (101721: 0.68 after 0, 0.15 if last=4 instead) -> noisy.
## Steer
- 3,1,6,4; mid-game 82289; 101721; 50331: zero / max steering change move probs by <=0.01. No measurable effect.
## Synthesis
- 4-move grid ending in 4: best 6,6,2,4 = 1.359 (dev max 1.618). 6-move extensions <=1.14. None beat dev max.
## Conclusion
Low confidence. The strongest signal is "opponent just played column 4 with column 5 empty", mainly in the opening; most threshold-level firing is unexplained. Looks like a mixture / possibly a random direction. No steering effect.
