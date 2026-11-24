# U12 notebook (layer 0, pole -, threshold 2.076, dev max 7.017)

## Examples (40, all bands)
Every firing example (bands 5-9) has last move in column 0. Band 4 (just below) also last col 0 but long games (ply 25-39).
Hypotheses:
H1: last move in col 0 and col 0 is tall (height >= 4).
H2: activation grows with col-0 height and falls with game length (ply), like a fraction of 0-tokens in the sequence.
H3: ownership pattern in col 0 matters.

## act tests
- First stone in col 0: strongly negative (-3 to -7). h=2: ~0-0.9. h=3: 1.6-3.1. h=4: 3.4-5.8. h=5: 4.3-6.
- Same h=4 col 0 with different owner patterns (ply 12): 3.8-4.0 for all; one (0,3,0,3,0,...) 2.38. H3 mostly rejected.
- Next move elsewhere (non-0) after a tall col0: drops to ~0. So it is about the last move.
- Ply sweep (filler moves before 0,0,0,0,0): h4: 4.3@16, 3.7@20, 2.1@24, 1.5@28, 1.2@32; h5: 6.0@17, 5.2@21, 3.6@25, 2.45@29, 2.2@33. H2 confirmed.
- Stones in cols 1-2 lower it a bit (1,1,1,1,2,2,2,2 filler: 2.46 vs 4.44 with cols 3/4/6).
Rule draft: last_col==0 and h - ply/9 >= 1.4.

## Scores
- s1 (p1: last col 0 and h - ply/9 >= 1.4): F1 0.733 (P .586 R .979) AUROC .979, sim share 0.53. FPs: h2 short games, h3, long games.
- s2 (p2: activation estimate 1.6h - 0.22*max(ply,16) + 1.4, h3 -0.9): F1 0.775 (P .643 R .974), AUROC .979, sim .54. FP: h6 late games overestimated, col1 full.
- act: full columns (esp. col 1, 2) lower it ~1.5-2; my ply sweep was confounded with full columns. Clean sweep (no full cols): h4 5.9@16, 2.7@28; h5 7.6@17, 4.2@29; h6 8.4@18.
- s3 (p3: with full-column penalties): F1 0.732 (P .742 R .722), AUROC .857, sim .44. Worse: penalties over-applied on dev; dropped.
- s4 (p4: v = h - ply/6 (h3 -1.5) >= 0): F1 0.800 (P .70 R .93), AUROC .960, sim .61.
  FPs had col 0 dominated by one colour (e.g. 0,3,0,3,2,4,4,4,0 col0 all O: 0.68).
## Colour composition (act, o = their stones in col0 incl. the last one, x = mine)
(o,x): (2,1) 2.5, (3,0) 0.5, (1,3) 1.6, (2,2) 3.8, (3,1) 3.4, (3,2) 4.3, (2,3) 3.1, (5,1) 6.2, (2,4) 1.7.
=> their stones in col 0 push it up (~1.3 each); my stones help up to as many as theirs, then hurt; no mine at all kills it.
- s5 (p5: colour counts only, no height gate): F1 0.690, sim .63. Height 2 FPs; height must stay in the rule.
- s6 (p6: p4 + penalty 1.3 per my col-0 stone beyond theirs, -2 if none of mine): F1 0.834 (P .833 R .836), AUROC .915, sim .65.
- s7 (p7: same, penalty 0.9): F1 0.841 (P .814 R .870), AUROC .932, sim .65. FINAL.
## Steer
4 positions, max and zero: changes <= 7 points, no consistent column (e.g. zeroing on 1,2,..,0x5 moves col3 +7, col4 -4). Effect weak.
## Synthesis
Spread opening (cols 1-6, no full columns, no fours) then 5-6 alternating stones in col 0 at ply ~17-20: 7.4-8.4, beats dev max 7.017.
