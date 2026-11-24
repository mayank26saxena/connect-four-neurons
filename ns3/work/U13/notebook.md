# U13 notebook (layer 5, pole +, threshold 0.931, dev max 78.2)

## Examples
- Bands 7-9 (11-78): almost all have the opponent's vertical three on top of column 6 (rightmost), cell above empty, opponent just played there (must-block in col 6).
- Band 6 (2-5): must-block in col 6 from a diagonal, opponent just played on top of col 6.
- Band 5 (~1-1.6): vertical three in col 0 (weak), misc.

## Hypotheses
H1: opponent vertical three in col 6 (open above). H2: any must-block in col 6. H3: generic vertical threat any column.

## act tests (minimal pairs)
- O vertical three col 6 (0,6,0,6,1,6): 31.7; with more stones under in col 6: 57. Same in col 0: 0.36, col 5: 1.04, col 1: 0.68, col 2/3/4: <0.1. => column 6 specific (H3 rejected).
- My own vertical three in col 6: 0.8 (no). Opponent horizontal three into (0,6): -11 (strongly off) => H2 rejected, vertical specific.
- Vertical three in col 6 but last move elsewhere: 5.9 (still fires, weaker).
- I also have an immediate win: 12.8-15 (reduced).
- Diagonal threat at (3,6) with O just played on top of col 6: 2.9; same threat, last move elsewhere: 0.3.
- Horizontal three at row 1 into (1,6) with O just played (0,6): 9.7; same threat when X filled (0,6) and O played elsewhere (position already lost): 0.3. Lost positions (double threats) suppress.

## Dev metric
- p1 (vertical three col 6 OR must-block in col 6 right after O played col 6): F1 0.549 (P 0.86, R 0.40), AUROC 0.70, sim share 52.7. BEST.
- p2 (+ vertical threes in any column after a move there): F1 0.347 (P 0.26). Other columns are noise -> dropped.
- p3 (vertical col 6 OR any opponent threat cell anywhere in col 6, single threat): F1 0.367. Too broad.
- p4 (vertical col 6 OR diagonal-only threat at col 6 landing after O played col 6): F1 0.529 (P 0.91, R 0.37). Horizontal ones also matter a bit.
- p5 (p1-ish + threat directly above col-6 landing, any last move): F1 0.440.
- p6 (vertical col 6 OR threat at/just above col-6 landing after O played col 6): F1 0.532.
Conclusion: core = opponent's vertical three on top of column 6 (40% of firing, nearly all strong activations). Rest of firing (act 1-5) is diffuse: diagonal/horizontal must-blocks in col 6, weak vertical threes in other columns (~1), various.

## Steer
- 0,6,0,6,1,6 (already plays col 6 at 1.00): max no change; zero -> col 6 0.98, col 0 +0.02.
- 3,3,4,4,0,5,0,5,3,0 (act 8): max -> col 6 from 0.00 to 1.00 (col 1 -0.93); zero ~no change.
- 3,1,4,2 (act 0.26): max -> col 6 from 0.00 to 1.00 (col 3 -0.97).
Effect: a strong "play column 6" (block on top of col 6) push.

## Synthesis (hill-climb with synth)
0,3,3,3,3,0,4,6,4,6,0,6 = 72.97 (dev max 78.2, not beaten); 0,3,3,3,3,0,2,6,4,6,0,6 = 72.2; 1,0,3,3,3,3,0,4,6,4,6,0,6 = 66.7; 2,4,6,6,2,6,2,2,4,6 = 65.1; 1,1,0,3,3,3,3,0,4,6,4,6,0,6 = 64.7.
