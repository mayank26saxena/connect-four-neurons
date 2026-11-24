# U12 notebook (layer 4, pole -, threshold 1.044, dev max 11.474)

## Observations (examples, ~70 viewed across bands)
- Top examples (6-10): 4,2,4,5,5 (6.7), 6,5,5,6,4,2,4 (9.3): opponent O at (0,4),(1,4),(1,5) with col 3 empty.
- Many firing mid-game positions contain an entirely empty column next to filled ones (col 3/4 often).
- Many ply-3 openings fire (0,6,4 = 4.4; 0,2,4 = 2.9): opponent has two bottom-row stones, not adjacent, me with one stone.
- Ply-3 exhaustive scan (ply3.txt): O at (0,0) corner raises it strongly unless X sits at (0,1) or on top of it.
- Steering: tiny, inconsistent effects (<0.1 prob).

## Hypotheses
H1: "well": an empty (or very low) interior column flanked by taller columns holding opponent stones.
H2: opponent stones spread along the bottom row with gaps (non-adjacent O's in row 0 / O in corner).
H3: no clean concept (mixture / random direction).

## Tests
- Minimal pairs on 4,2,4,5,5 (6.7): shifting the same shape one column left/right or mirroring it -> ~0. Highly position-specific.
  O at (1,5) over X(0,5) fires (8.7); X at (1,5) over O(0,5) does not (0.6).
- Filling the "empty well" column does not kill firing (4,2,4,5,5,3,6 = 10.2) -> H1 rejected.
- Ply-3 scan (ply3.txt): almost every firing opening has O at (0,0) with (0,1) not X, or O at (0,4) plus O at (0,1)/(0,5). Ply 2: nothing fires.
- Cell histograms (160 firing vs 160 non-firing sampled examples): firing positions almost never have X at (3,3), X at (2,4), O at (3,4), O at (0,2); enriched for X at (0,2), O at (2,4)/(3,3)/(2,5).
- But interactions flip sign: in mid-game 2,2,5,3,...,4,5 an O at (2,4) raises it (6.1 -> 8.3) and an X lowers it (3.0); in 4,5,5,2,4 an X at (2,4) gives 4.1 and an O gives 1.1.
- Firing spread over all plies (0-40) and both sides to move.

## Score calls
1. p1 well depth>=2: F1 0.045, AUROC 0.447, sim -0.00. Rejected.
2. p2 linear cell template: F1 0.149, P 0.11, R 0.23, AUROC 0.588, sim 0.02.
3. p3 veto cells + template (>=3): F1 0.169, P 0.10, R 0.49, AUROC 0.678, sim 0.03. (best)
4. p4 same, threshold 4: F1 0.167, AUROC 0.627.
Stopped at 4 calls: no hypothesis gets past weak cell-level correlations; looks like a mixture / possibly a random direction.

## Steering
Zeroing: mostly <0.05 prob change (8.7, 6.5, 8.7 activations). Exception 4,2,4,5,5,3,6 (10.2): zeroing raises col 3 +0.35, lowers cols 0/1. Max-forcing on low positions: <0.1 changes, no consistent column.

## Synthesis
4,5,5,3,4,2,6 = 10.54 (best), 4,5,5,3,4,2,6,1,0 = 10.32, 4,2,4,5,5,3,6 = 10.17, 4,5,5,2,4,3,6 = 10.10, 6,5,5,6,4,2,4 = 9.27. None beats dev max 11.47.
