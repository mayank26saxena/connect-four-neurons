# U72 notebook (layer 0, pole +, threshold 1.029, dev max 2.901)

## Observations (120 examples, 3 seeds + default)
- Every firing example has last move in column 6 (opponent just played the right edge).
- last=6 alone is not enough: early game (ply<10) ~0; ply 15-30 fires; very late (ply>30) and tall col 6 (5-6 stones) weak.
- act test on top game prefixes: appending 6 at ply 5,7,9,11,13,15,16,17,18 -> 0.08,0.05,0.15,0.56,0.77,1.10,1.98,2.17,2.30. Rises with ply.
- Earlier 6s in history lower it somewhat (2.30 -> 2.0 / 1.5 / 1.3 with 1-2 extra 6s).
- Last move in col 5/0/4 instead of 6 at same position: 0.2/0.3/-0.03.
- Extending ply before the 6: 18->2.30, 20->2.56, 22->2.71, 24->1.94, 26->2.02, 30->1.57 (peaks mid game).

## Hypotheses
H1: last move col 6, ply in mid game (~15-31), column 6 low (<=4 stones incl. new one).
H2: same but graded: level ~ ply closeness to ~22 minus height of col 6.
H3 (alt): count of other columns' stones (board fullness) rather than ply (same thing for layer 0).

## score 1 (p1: last=6, 15<=ply<=31, h6<=4): F1 0.558 (P 0.42, R 0.83), AUROC 0.90, sim share 0.43
FPs include ply-15 positions with col 4 empty; misses include tall col 6 but col 5 empty.

## Token-substitution scans (replace earlier move i by column c, keep final 6)
- Top game (h4=3): any 4 replaced by another col: -0.6..-0.9. Any 5 replaced: +0.2..+0.3. 3 replaced: ~+0.1-0.2. Parity of mover irrelevant.
- Low game 21814 (h4=6, full): removing a 4 RAISES by +0.4..0.8. -> col 4 effect is non-monotone, peak near 4 stones.
- Direct: top game + extra 4s: h4 3->4 +0.4, 4->5 -0.5, 5->6 -0.6.
- Cols 0/1/2 stones add a little (~+0.1 each); col 5 and earlier col 6 stones subtract.
H2': last=6 AND col 4 moderately filled (2-5, peak 4) AND col 5 / col 6 not tall; activation grows with total stones in cols 0-2.

## score 2 (p2: last=6 and weighted column score >= 1.3): F1 0.466 (P 0.31, R 0.96), AUROC 0.945, sim 0.47
Ranking much better; threshold too low; FPs are long games (ply 30+) and early ply-10. Add late-game penalty, raise threshold.

## score 3 (p3: p2 + penalty for ply>24, threshold 1.75): F1 0.598 (P 0.50, R 0.74), AUROC 0.86, sim 0.44
Late penalty hurt ranking (misses at ply 26-28). FPs still include ply-9 positions (h4=3 but early). Next: drop ply penalty,
cap cols 0-2 contribution (long games), add early-game ramp, threshold ~1.6.

## score 4 (p4: capped counts + early ramp, thr 1.6): F1 0.628 (P 0.49, R 0.87), AUROC 0.92, sim 0.53
FP 12515: col 4 full at ply 15 -> act -0.5; misses: col 4 full at ply 26-30 still fire. => it's the FRACTION of moves in col 4.
## Fixed-ply-18 scan of col-4 count (substituting moves): h4 0:-0.2, 1:0.5, 2:1.6, 3:2.3, 4:2.1, 5:1.6, 6:0.84.
Col 5 count not reliably negative (h5 0 vs 4: 1.9 vs 2.3). Peak when ~17-20% of moves were in col 4.
Ply ramp: same fraction at ply 11/13/15/16 -> 0.56/0.77/1.1/1.98.
H3: act ~ ramp(ply) * C(share of moves in col 4) - 0.25 per earlier col-6 stone, only when last move col 6.

## score 5 (p5: pure col-4 share curve x ply ramp): F1 0.578 (P 0.44, R 0.84), AUROC 0.90, sim 0.54
Worse detection than p4. Pure share misses positions with 4-5 col-4 stones at ply 15-17 that still fire. Back to p4 counts,
but make the penalty for many col-4 stones depend on their share (full col 4 hurts at ply 15, not at ply 28).

## score 6 (p6: p4 + share-dependent col-4 penalty, thr 1.6): F1 0.516 (P 0.35, R 0.98), AUROC 0.959 (best), sim 0.54
Best ranking so far but threshold far too low (fires on 8.5%). Next: same score, threshold 2.0.

## score 7 (p7: p6 with thr 2.0): F1 0.533 (P 0.38, R 0.88), AUROC 0.92, sim 0.54
Still fires 7%; FPs are late games with column 6 filled to 5-6 stones. Earlier col-6 stones need a much bigger penalty
(p1's h6<=4 cutoff, act tests: two extra 6s 2.3->1.3). Last call: p6 score with -0.35 per earlier col-6 stone, thr 1.8.

## score 8 (p8: p6 with -0.35 per earlier col-6 stone, thr 1.8): F1 0.594 (P 0.48, R 0.77), AUROC 0.87, sim 0.53
Budget exhausted. Best F1 = p4 (0.628, sim share 0.53) -> final program.

## Steering (3 firing positions, set to dev max and to 0): move-probability changes <= 4 points; effect none measurable.

## Synthesis (all beat dev max 2.901): 3.126, 3.124, 3.088, 3.038, 2.910. Recipe: ply ~19, last move col 6 (first col-6 stone),
4 of the 18 earlier moves in col 4, many in cols 0-2, no earlier col-6 stones.

## Conclusion
Layer-0 unit: gated by "opponent just played column 6"; strength set by move-history composition (share of col-4 moves
peaking ~1/5, mid-game ply ~16-28, few earlier col-6 moves). Looks like a token/count feature rather than a tactical concept.
Confidence medium (F1 0.63; minimal pairs consistent; exact strength curve only approximated).
