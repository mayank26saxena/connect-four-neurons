# U57 notebook (layer 2, pole -, threshold 0.562, dev max 7.347)

## Observations
- Top-band examples: almost all have opponent (O) stones at (0,4) and (1,4) (bottom two cells of column 4).
- steer to zero / max: changes move probs by <= 0.01 in 6 positions. Effect essentially none.
- Minimal pairs on 3,3,4,5,3,1,1,6,x: prefix is non-firing (other perspective), nearly every O move fires except x=5 (0.33).

## Hypotheses
H1: opponent owns bottom two cells of column 4.
H2: H1 plus some context on col 3 / col 5 (e.g. col 5 cell (1,5) empty / not O).
H3: random direction / mixture.

## Tests and scores
- Minimal pairs: base 4,6,0,6,4 (opponent pair at bottom of col 4, 1.8). Pair belongs to mover -> no fire (4,6,4,6 = -0.17); same pair for opponent (6,4,0,4) fires. Pair in cols 1/2/3/5 does not fire. Opponent stone on (1,5) kills it (-0.43); opponent stones in col 1 or col 6 lower it; my stones in col 2 raise it. Many dev firings lack the pair, though.
- s1 p1 (opp owns (0,4),(1,4)): F1 0.112, P 0.068, R 0.31, sim -0.02.
- s2 p2 (+ no opp on (1,5), no my col-3 pair, ply<=22): F1 0.161. The col-3 exclusion was wrong (miss 65170).
- s3 p3 (opp owns (0,4), broad): F1 0.131, R 0.40.
- s4 p4 (pair + no opp on (1,5) + ply<=20): F1 0.193, P 0.157, R 0.249, sim 0.03. Best.
- steer: about 0.01 in 6 positions; in one position, zeroing it moved 0.10 from col 6 to col 5.
- Synthesis: greedy search reached 7.327 (3,3,4,5,3,1,1,6,4,6,2,5,1), just below the dev max of 7.347.
- Conclusion: low confidence. Opponent stones low in column 4 are the clearest ingredient, but firing depends on many cells, so it looks distributed or mixed.
