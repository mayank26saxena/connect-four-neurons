# U05 notebook (layer 3, pole -)
## Examples
- All 150 sampled positions in bands 4-9 have column 4 height exactly 2 (landing cell (2,4)). Band 3: 20/30. Bands 0-2: rare.
- Within col4 h2, activation is very sensitive to colours/other stones (minimal pairs): e.g. 3,3,3,5,5,4,4 = 1.89 but 3,3,5,5,3,4,4 = -0.73 (col5 colours swapped).
## Hypotheses
H1: fires iff col 4 has exactly 2 stones (necessary; modifiers unknown).
H2: modulated by neighbouring columns 3/5 heights or colours around (2,4).
H3: modulated by parity / which side to move.
## score 1 (p1: col4 h2): F1 0.364 P 0.223 R 1.0 AUROC 0.946, sim share 0.33
## Histograms within col4-h2 positions by band
- col5 height 0/1: band3 46%, band0 85%, band9 6%, band5 19% -> require col5 >= 2.
- (1,4) = theirs enriched in top band (81% vs ~51%); last move col 4 enriched in top band.
- act: 3,3,3,0,0,4,4 = -0.43, 3,3,3,6,6,4,4 = -0.40, 3,3,3,5,5,4,4 = 1.89 (col5 stones needed); colours in col5 matter too.
## score 2 (p2: col4 h2 & col5 h>=2): F1 0.486 P 0.352 R 0.782 AUROC 0.869, sim 0.48. Misses had tall col 3 but short col 5.
- act: col3 alone tall with col4 h2 raises gradually (0.67 -> 1.74), not enough alone; colours of flanks matter a lot (3,5,3,5,4,4 = -3.35 vs 5,3,5,3,4,4 = -0.23).
H4: crowdedness: count filled cells among (1..3, 3) and (1..3, 5) beside (2,4), >= 3.
## score 3 (p3: col4 h2 & >=3 filled flank cells): F1 0.480 P 0.324 R 0.919 AUROC 0.930, sim 0.49. Many FPs at 1.5-1.9.
- Key minimal pair: 3,3,3,5,5,0,5,4,4 = 3.09; +6 (flips who is to move, so all colours swap) = -0.59; +6,6 = 2.38; 3,3,3,5,5,0,5,6,4,4 = -3.03.
  => strongly depends on colour relative to the mover: opponent stones around (2,4) push up, my stones push down.
H5: col4 h2 and (#their - #my stones among the 7 filled-able neighbours of (2,4)) >= 2.
## score 4 (p4 colour difference): F1 0.225 -- rejected; colour effects are not a simple their-minus-mine count.
- More minimal pairs at ply 9 (same occupancy, different colours): 4.65 / 3.09 / 2.65 / 1.26 / 0.16 / -1.17. (0,5)=mine and (1,4)=theirs over (0,4)=mine seem to help; no clean rule.
- Flipping the side to move by one extra far-away stone always drops activation (3.09 -> 0.78, -0.12, -0.57); restoring parity with a second stone brings it back (1.4-5.0).
H6: score = flank-filled count + 1 if col5>=2 + 2 if last move in col 4; fire if >= 5.
## score 5 (p5): F1 0.499 P 0.379 R 0.733 AUROC 0.848, sim share 0.58 (best so far).
- steer (zero): small effects; in strong cases removing the unit lowers col 4 (the (2,4) landing) by 4-12 points; in others +-5 on col 3/4/5. Inconsistent.
H7: p5 + 1 point if (1,4) (stone under the landing cell) is the opponent's; threshold 6.
## score 6 (p6): F1 0.471 P 0.367 R 0.659, sim 0.51 -- worse than p5; keep p5.
## Synthesis (act hill-climb by stone insertions/substitutions, synth checked)
- 3,5,3,3,5,0,5,0,6,4,4 = 6.24; 3,5,3,3,5,0,5,0,6,6,3,4,4 = 8.74; 3,5,3,3,3,0,5,0,6,6,5,4,4 = 9.05; 3,5,3,3,3,1,5,0,6,6,5,4,4 = 9.18 (dev max 9.506).
- Pattern of the climbed positions: col 4 has two stones (mine at bottom, theirs on top, just played), cols 3 and 5 stacked 3-4 high around the empty (2,4).
## Conclusion
Column 4 having exactly 2 stones is necessary (recall 1.0) but only ~22% of such positions fire. Firing gets more likely when columns 3 and 5 are stacked beside the empty (2,4) and when the opponent just played the 2nd stone in col 4. The colours of the nearby stones relative to the mover matter a lot (flipping the mover swings it by 3-4), but I found no simple colour rule. Confidence medium-low (F1 0.50).
- Final climb: 3,5,3,3,3,1,5,1,6,6,1,4,4 = 10.04 BEATS dev max.
