# U73 notebook (layer 0, pole +, threshold 0.001, dev max 0.007)
## Examples
Almost all firing positions are very early (ply 4-6); top band (99.9%) is entirely ply 4 with last move in col 0 or 1.
Hypotheses:
H1: opening-stage detector: ply 4 (second player just moved), strongest when last move is in left edge cols 0/1.
H2: last-column token detector (cols 0/1) independent of ply. -> rejected by act: ply 7+ with last col 1 gives ~0.
H3: parity: fires after second player's moves (even ply) more than odd.
## act tests
- prefix 3,4,5 + c: c=0 .006, 1 .007, 2 .002, 3 .003, 4 .001, 5 .004, 6 .001. Similar for 2,0,5 / 6,6,6 / 3,3,3 / 0,1,2.
- ply 5 (prefix of 4) + c: col 0/1 ~.002-.003, col 5 ~.001-.002, others ~0.
- ply 6 + c: col 0/1 ~.002, others <=.001. ply 7: all ~0; ply 8 col 0/1 .002; ply 9: ~0.
=> Activation ~ (column weight: 1>0>5>3>2>4,6) x (decays fast with ply; even ply > odd).
## score 1 (p1: last-col weight minus ply decay): F1 0.624 P 0.507 R 0.811 AUROC 0.894. Simulation nan (ceiling negative, ablation baseline odd).
## More act tests
- Order of earlier tokens does not matter (0,6,6,1 == 6,6,0,1): bag-of-tokens, consistent with layer 0.
- At even ply, the first player's ("my") earlier stones matter: cols 3/5 raise (~+1 mil each), col 0 lowers (~-1), col 4 lowers a bit.
  e.g. 3,4,5,1 .007 vs 6,6,6,1 .004 vs 0,6,6,1 .003; 3,4,5,2 .002 vs 0,2,4,2 -.000; 3,6,5,6,3,1 .002 vs 0,6,4,6,0,1 -.002.
- Opponent's earlier stones barely matter. At odd ply other stones barely matter (3,6,5,6,1 == 0,6,4,6,1 = .002).
H4: s = W[last col] + sum over my stones M[col] (even ply only) - D(ply).
## score 2 (p2, H4): F1 0.763 P 0.783 R 0.744 AUROC 0.869. Misses at ply4 last col 3/5 -> raise W3,W5; FPs last col 2/4 -> lower. p3 = recalibrated weights, graded level.
## score 3 (p3): F1 0.784 P 0.801 R 0.768 AUROC 0.881. FPs at odd ply (6,4,5,0,1): act shows my-stone weights apply at odd ply too (6,3,6,5,1 .004 vs 6,0,6,4,1 -.001). Positive my-stone sum saturates; their col-0 stones +small. p4: M at all plies, cap +2, per-ply decay table.
## score 4 (p4): F1 0.780 P 0.799 R 0.761 AUROC 0.878 (no gain over p3; residual errors are near-threshold, act resolution 0.001). Keep p4 (matches act tests).
## steer: 3,4,5,1 / 2,0,5,0 / 6,3,6,5,1 -> no measurable change in move probabilities (activation range is only ~0.007).
## synth: 3,0,5,1 and 5,0,3,1 beat dev max (0.007); 3,4,5,1, 3,1,5,0, 5,4,3,1 tie.
Conclusion: layer-0 bag-of-tokens direction, tiny magnitude, no effect. Possibly a random direction. Confidence medium.
