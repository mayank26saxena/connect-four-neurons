# U08 notebook (layer 0, pole -; threshold 1.806, dev max 4.666)

## Examples (ex1.txt, ex9.txt)
- Nearly every firing example has column 0 completely full (height 6). Top band: mostly last move = col 0 filling it.
- Band 3-4 (just below threshold) also often have col 0 full but more moves since.

## Hypotheses
H1: fires when column 0 is full. Strongest right when the last move filled it.
H2: fires when last move in col 0 (any height) -- rejected by act: col0 heights 1-4 last move col0 gives ~ -0.5..0.
H3: any full column -- rejected: col 6 full -> 0.21, col 1 full -> 0.21.

## Minimal pairs (act)
- 4,0,6,0,0,4,3,5,1,2,0,3,0 (col0 h5): 0.76; +0 (h6): 3.62 FIRES; +6: 1.75; +6: 2.31.
- 0,1 alternating: col0 h5 after last move 0: 0.92; h6: 2.47.
- col0 filled after 10 other moves: 3.99, stays 2.2-3.8 for next 6 moves.
- col6 full, col1 full (col0 empty): ~0.2. Col 0 full + col1 full: 2.0-2.8.
- Opening 0,0,0 gives 2.5-7 (fewer than 4 stones not scored; 0x4..0x6 fires heavily).

## score 1 (p1: col0 full): F1 0.407, P 0.256, R 0.994, AUROC 0.954, sim share 0.16
Col 0 full is (almost) necessary but only ~26% of col0-full positions fire.
## More act tests
- Activation highest right after the move that fills col 0 (k=0). Decays after; parity effect (odd k lower).
- Early fill (ply 14-16) stays 2-3.8 for >10 moves; late fill (ply 30) 3.86 -> 1.29 after 4 moves.
- Fill at ply 36 -> 1.97, ply 38 -> 1.38, dev pos at ply 39 -> 0.06. Strong ply (board fullness) penalty.
- Spread-out vs consecutive col0 moves: both fire (3.09 vs 3.9 at ply 30). Other full columns: little effect.
- Openings dominated by col0 moves (0,0,6,0,0,0) fire 4.3 even with col0 h5; rare.
## score 2 (p2: col0 full and k<=2 or (k<=10 and fill ply<=20)): F1 0.536, P .41 R .76, sim .14
## score 3 (p3: linear estimate 4 - 0.3*max(0,F-28) - 1.3[k>0] - 0.4[k odd] - 0.04*k*max(0,ply-24) > 1.8): F1 0.748 P .71 R .79 AUROC .89 sim .13
## score 4 (p4: k>0 uses ratio 24*(6/ply-0.125), k=0 slope 0.2, opening rule): F1 0.711 P .64 R .80, sim .18
## score 5 (p5: average of p3/p4 for k>0, slope 0.3 at k=0): F1 0.748 P .715 R .785, sim .14 -> plateau; choose p3-style (p5) as final.
## Steer (5 positions, max and zero): changes <= 0.06 prob; effect none measurable (col 0 is full so the move it concerns is already illegal).
## Synthesis: 0,0,0,0,0,0 -> 6.95; 3+0x6 -> 5.09; 0x6+1 -> 4.92; 6+0x6 -> 4.89; 0,0,6,0,0,0,0 -> 4.85 (all beat dev max 4.666)
## Confidence: F1 0.75, act tests agree, board pattern (col 0 full) with a graded timing/fullness modifier -> high-ish; but the
## magnitude model is a hand-tuned approximation and sim share is low, so I report medium-high -> 'high' per rubric? Rubric says high if F1>=0.7 and board pattern. Choose high.
