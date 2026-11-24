# U06 notebook (layer 5, pole +, threshold 0.711, dev max 41.3)

## Observations
- Bands 7-9 (act 4-41): nearly all = opponent's last move in column 5 made a vertical three there; must-block cell directly above in col 5.
- Bands 5-6 (0.7-4.3, two thirds of firing!): mixed. Many have a must-block in another column (often a vertical three in col 1/4/6), some have last move in col 5 without a threat, some early openings (4,2,4,1).
- act: 5,0,5,3,5 -> 29.1; same pattern in col 6 -> 1.2, col 1 -> 0.76, cols 0,2,3,4 -> ~0. Horizontal threat at (0,5) -> no firing. My own vertical three in col 5 -> 0.29.

## Hypotheses
H1: opponent vertical three (just played) with cell above empty; col 5 strong, other columns weak.
H2: any must-block (opponent immediate threat), col 5 strongest.
H3: last move in col 5 plus some threat.

## Score log
- s1 p1 (last move col5 making vertical three): F1 0.408, P 0.968, R 0.259. Sim share -18 (ceiling only 17.4%). FPs: I have own win, or position already lost / one legal move.
- s2 p2 (vertical three just made, any column, col5=9 others=6): F1 0.294, P 0.227. Other columns mostly do NOT fire -> column 5 specific.
- s3 p3 (last move col5 and cell above it is a must-block, any line type): F1 0.468, P 0.69, R 0.354.
- s4 p4 (any must-block in col5, no own win elsewhere): F1 0.461, P 0.53, R 0.41. FPs: low threat rows (0-2), horizontal threes.
- steer: forcing max pushes column 5 to ~1.0 (e.g. 4,2,4,1: col3 0.76 -> col5 1.00; late-game FP: col4 0.99 -> col5 0.76). Zeroing barely changes forced blocks.
- s5 p5 (must-block in col5 at row >=3, no own win elsewhere): F1 0.478, P 0.735, R 0.354. BEST.
- s6 p6 (p5 + row-2 threat above last stone, level 0 for my col5 win): F1 0.460. Worse. Sim share stays ~ -18 for every level scheme tried (ceiling 17.4%, so unit's ablation effect is small and my level readings never help).
- Recall ceiling: two thirds of firing is the weak band 0.71-4.3, which is diffuse (band 5 looks like band 3: ~25% must-blocks, last col spread). Other-column vertical threats fire weakly and inconsistently (col 1/4/6 ~1-3, cols 0,2,3 ~0).
- Synthesis: best 38.7 (dev game 12634), 37.8 variant, 34.0 for 5,5,0,5,6,5. None beat 41.26.
## Conclusion
Column-5 must-block detector (strongest for vertical three in col 5 just played); pushes the model to play col 5. Medium confidence: strong part is clean, weak band unexplained.
