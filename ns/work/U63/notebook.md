# U63 notebook (layer 0, pole -, threshold 0.003, dev max 0.009)

## Exploration
- Top bands (8-9) are entirely ply-1 positions: opening in col 6 (0.009), col 5 (0.006). Opening col 0 = 0.003 (just fires);
  cols 3,4 = 0.003 just under; col 1 0.002; col 2 0.000. Ply 2 never fires (all 49 pairs <= 0.000).
- Bands 5-7 also contain many mid/late-game positions with no obvious tactical theme (no wins/blocks pattern).
- Counts over ~750 sampled examples: firing mid-game last col 3/0/6 somewhat over-represented; even ply slightly over-represented.
- Minimal pairs: changing only the last move shifts activation additively: last col 0/3/6 high, 2/5 low (two contexts).
- Context: "3,2,3,2,3,3" 0.004 vs "1,2,1,2,1,3" 0.000: first player's earlier stones in col 3 raise it; opponent's earlier
  moves in 2/6 raise it vs 0/4. Effects small and interacting (layer-0 attention averages over tokens).
- Late-game firers often have col 3 (centre) empty or nearly empty while other columns are full.

## Hypotheses
H1: ply 1 and opening in col 5 or 6 (or 0). Covers the top but probably low recall.
H2: H1 OR (last move in col 0/3/6 and centre column has many stones of the player to move ...) -- additive token mix.
H3: no clean concept: a layer-0 mixture of last-token identity + attention-averaged move tokens (random-direction-like).

## Score calls
1. p1.py (H1: ply==1 and opening col in {0,5,6}; level by opening col): F1 0.593 (P 1.000, R 0.421), AUROC 0.711;
   simulation share of ceiling 4.18. All misses are mid/late-game positions.
2. p2.py (H1 + "first player... my stones dominate col 3, last col 0/3/4/6" + "late game, col 3 nearly empty"):
   F1 0.226 (P 0.137, R 0.633). Mid-game rules fire on 12.7% of positions; far too broad. Dropped.

## Decision
Mid-game firing (~58% of firing) is diffuse: small additive effects of the last move's column (0/3/6 up, 2/5 down) and of
earlier stones (player-to-move's stones in col 3 up), all near the 0.003 threshold. No clean board rule found; I keep H1.
Activations are tiny (max 0.009). Steering (6; 3,2,3,2,3,6; 4,1,0,4,3,6,3,3) to max or zero changes no move probability
(all +/-0.00). Synthesis: cannot beat dev max 0.009 (the single opening 6 reaches it; best constructed mid-game 0.007).

## Synthesis revision (orchestrator audit)
3,2,3,2,3,2,3,6 and 3,2,3,2,3,2,3,4,4,6 completed a vertical four in col 3 on move 7 (game over). Replaced with
3,2,3,2,3,2,4,6 (synth 0.006) and 3,2,3,2,3,2,0,3,4,6 (synth 0.006); checked with facts that no move completes a four.
Kept [6] (0.009), [5] (0.006), 3,2,3,2,3,2,0,6 (0.007). None beats dev max 0.009. No extra score calls used.
