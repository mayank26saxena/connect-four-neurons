# U27 notebook (layer 0, pole +, threshold 0.004, dev max 0.014)

## Examples (bands 0-9, ~150 firing examples)
- Top band dominated by ply 5 (me = second player), last move mostly col 3; also ply 24 and ply 40 late games.
- Firing ply distribution bimodal: ply 5-9 early, 17-28 middle, 32-41 late.
- Last col of firing examples drifts with ply: early -> cols 0-4 (not 5,6); middle -> cols 0-3; late -> cols 4-6.

## Hypotheses
H1: position/token unit (layer 0): fires when ply is 5 or 7 and last move not in cols 5-6; or late (ply>=32) and last move in cols 5-6; or middle (ply 19-28) and last move in left cols 0-3.
H2: some board-shape feature (column heights / filled right side) -- no clear evidence.
H3: random direction / mixture.

## act tests
- 4,1,5,3,x at ply 5: x=0..4 all fire (0.007-0.012), x=5 0.002, x=6 0.003. Varying moves 1-4 keeps firing (0.007-0.014). Ply 5 is robust if last col <= 4.
- Ply 4/6 after same prefix ~0.000; ply 7 fires again (0.005-0.010). Odd early plies.
- Random games (30, my generator gen.py): fire rate by ply: ply5 7/30, ply7 3/30, ply 23-24 ~2/30, ply 37-40 rising to ~50%.
- Ply 5 random: first move 4 helps; last move 5/6 kills; 3,3,3,3,2 -> 0.004 (stacking in center hurts).
- Ply 24 last-col sweeps on 3 games: cols 0-3 > 4 > 5,6, but one game is ~0 everywhere -> strong game context effect not captured.
- Ply 36 sweeps: cols 5,6 ~0.004 > others ~0.001.

## More act tests
- Same board, different last move (4,0,5,0,3 = 0.013 vs 3,0,4,0,5 = 0.002): depends on last move, not just board. Earlier move order irrelevant (4,0,5,0,3 = 5,0,4,0,3).
- Ply 5 composition (small, about +-0.002 to 0.004 each): opponent stones in cols 4-5 up, my stones in col 0 up, my stones in cols 4-6 down. Holds at ply 6 too from the mover-relative view (4,0,4,0,3,3 = 0.000).
- Stacking col 5 early does not rescue last-move-in-5 (5,5,5,5,5 = 0.000): row is not the factor.
- Full sweeps (every legal last move at every ply, games g3, g9): col 3 best at plies 4-11; mid-game alternates between left-favoured and right-favoured plies with game-specific parity; plies 30-37 favour cols 5-6. Looks like a sequence-position x last-token interaction (layer 0), not a clean board concept.
- steer max/zero on 5 positions (ply 5 openings, ply 40 endgame): change in every column is 0.00. No measurable effect.

## Scores
1. p1 (ply 5/7 & col<=4; ply 19-28 & col<=3; ply>=34 & col>=5): F1 0.188 (P 0.105 R 0.893), AUROC 0.830, sim share 0.73. Mid-game branch floods false positives.
2. p2 (drop mid branch, late ply>=36): F1 0.418 (P 0.297 R 0.706), AUROC 0.827, sim -0.06 (bad level).
3. p3 (add composition count): F1 0.389, AUROC 0.794, sim -0.47. Composition hurt; dropped.
4. p4 (p2 fires + p1 level): F1 0.418, sim share 0.73.
5. p5 (add ply 6 & col 3; late ply>=37): F1 0.423 (P 0.297 R 0.736), AUROC 0.841, sim share 0.73. FINAL.

## Synthesis
4,0,5,3,3 / 4,0,4,3,3 / 5,0,4,3,3 / 4,3,4,0,3 all 0.014 = dev max (not above). 4,0,5,0,3 0.013.

## Conclusion
Fires mainly at the opening (5-7 stones, opponent just played a column 0-4, best the centre column 3), and at the end of the game (37+ stones, opponent just played column 5 or 6). Two regimes with opposite column preferences, plus weak stone-composition effects and parity effects mid-game. No steering effect. Confidence low: it looks like a position-and-last-token mixture (possibly a random direction).
