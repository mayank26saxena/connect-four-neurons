# U30 notebook (layer 3, pole -, threshold 1.995, dev max 6.087)

## Exploration
- All ~60 firing examples (bands 5-9, 3 seeds) have column 1 with exactly ONE stone (landing cell (1,1)). Bottom stone can be either colour.
- Many near-threshold non-firing (bands 3-4) also have col1 h=1 -> strength is modulated by context.
- act: 61725 jumps -3.6 -> 4.0 when the 12th move goes into col 1 (col1 0->1). A 2nd stone in col1 kills it (-1.1).
- Empty-ish board with col1 h=1: ~0 (no fire). More stones elsewhere raise it; stones in cols 0 and 2 raise most (,0,0,2,2 -> 4.4; full cols 0 and 2 -> 4.8). Stones in cols 3/6 do little.
- Col1 h=0 with full cols: no fire; playing any other column: no fire.

## Hypotheses
H1: fires iff heights[1]==1 and enough stones on board (esp. in cols 0 and 2).
H2: heights[1]==1 and cols 0,2 tall (neighbors of cell (1,1) filled).
H3: specific colour pattern around (1,1).
- score p1 (h1==1 & h0+h2>=3): F1 0.425 P 0.277 R 0.914 AUROC 0.919, sim share 0.64. (accidentally used 2 calls; call 2 was a duplicate re-run)
- Counts over 230 col1-h1 examples (8 seeds): fewer open columns -> higher (legal=7: 38% fire, <=4: ~95%); col2 full 92%, col3 full 83%; last move in col1 94%; bottom stone in col1 theirs 77% vs mine 55%.
- act: 3x6 (col3 full)+1 -> 1.5 vs col3 h5 -> 0.34; cols 3,2 full + 1 -> 3.5.
H4: col1 has one stone AND the board has full columns (esp. 2/3); boosted when last move was col1.
- score p2 (h1==1 & (full col or last col1)): F1 0.478 P 0.339 R 0.813, sim 0.65
- counts: total stones (ply) is the main modulator among col1-h1 positions (ply<10: ~0% fire; ply>=20: >80%).
- score p3 (h1==1 & ply+2*full+6*last1 >= 18): F1 0.581 P 0.44 R 0.853 AUROC 0.909, sim 0.72
- misses of p3 all had col3 height 5 with low ply. act on 25562 (3,3,1,4,3,3,3,2,0): col3 h5 2.07, h4 1.45, h3 0.49. Colour of the col1 bottom stone barely matters (swap: 2.32 vs 2.07). But adding a far stone (0,6) kills it (0.7/-0.03) -> colour-relative/parity effects I cannot capture simply.
- score p4 (+4 if col3 h>=5, thr 20): F1 0.592 P 0.45 R 0.866, sim 0.73
- score p5 (weighted heights h3 + .5(h0+h2), thr 23): F1 0.573, sim 0.72 -> worse
- score p6 (= p4 with thr 23): F1 0.596 P 0.483 R 0.778, sim 0.73. Plateau ~0.6; remaining errors look colour/parity-dependent.
## Effect (steer)
- 61725: max -> col1 -3 pts; zero -> col1 +6. 140880: zero -> col1 -8, col5 +6. Three other positions: changes <= 3 pts. Effect is small and sign-inconsistent on column 1.
## Synthesis
- Cols 0,2,3 full + one stone dropped last into col 1: P=0x6,2x6,6,3x6 then ,5,5,1 -> 6.741 (beats 6.087); ,5x6,1 -> 6.33; ,4,4,1 -> 6.21; ,5,5,6x4,1 -> 6.22.
## Final: p6, F1 0.596, sim share 0.73, confidence medium.
