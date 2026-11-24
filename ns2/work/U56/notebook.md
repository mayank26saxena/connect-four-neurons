# U56 notebook (layer 2, pole -)
## Observations
- Top examples: early game, bottom-left corner. Often (0,0) empty, (0,1)=them, (0,2)=me. Column 0 alternating me,them,me,them from bottom gives very high (0,1,2,0,0,0 => 5.4).
- Steer to zero: negligible change in move probs (<=0.02).
- act: (0,1)=t alone insufficient; (0,1)t+(0,2)m gives ~0.7-1.5; (0,4)=m lowers; col0 m,t,m,t alone ~2.2 (parity matters: t,m,t,m ~0).
- Not left-right symmetric (mirror patterns ~0).
## Hypotheses
H1: (0,1) theirs and (0,2) mine (and (0,0) not theirs).
H2: checkerboard colouring of bottom-left corner: me on (r+c) even, them on odd, for cells in col 0 and row 0 cols 0-3.
H3: column 0 alternating starting with me at bottom.
## Scores
- p1 H1 (0,1)t & (0,2)m & (0,0)!=t: F1 0.117 (P .07 R .31), sim 0.00. Too broad (late game).
- p2 (0,0) empty & (0,1)t & (0,2) filled: F1 0.230, sim 0.06.
- p3 hand-weighted corner score (col0 alt bonus, (0,4) penalty, ply>12 penalty): F1 0.282, sim 0.07.
- Histograms (single features by band): firing boards are early (60-90% ply<=11), col0 empty (78% vs 20%), (0,4) empty (64% vs 19%), cols1-3 bottom filled.
- p4 col0 empty & col4 empty & cols1,2,3 non-empty: F1 0.374 (P .39 R .36), sim 0.10. Best F1.
- p5 additive score variant: F1 0.342.
- p6 p4 (ply<=16 or (0,1) theirs) OR early (0,1)t/(0,2)m with col0 empty: F1 0.372, AUROC .687, sim 0.13. Submitted.
## Minimal pairs (act) notes
- Very context sensitive: same 4-stone core changes by >1.5 with far-away filler stones; parity relative to mover matters (col0 me,them,me,them fires ~2.2; them,me,them,me ~0).
- (0,0) filled (non-alternating) kills; (0,4) filled lowers; mirror patterns on right side ~0.
## Steer: negligible (<=0.03 prob change) on 7 positions, to zero and to max.
## Synthesis: 3,0,1,2,0,0,0 = 5.572 beats dev max 5.400.
## Conclusion: low confidence; looks distributed, possibly a random direction loosely tied to an early-game bottom-left cluster.
