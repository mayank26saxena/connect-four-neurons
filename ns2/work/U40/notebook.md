# U40 notebook (layer 4, pole -)
## Observations
- Top examples: late, crowded boards, few legal columns; often one near-empty column with stacked threats.
- facts on 7 top examples: teacher scores almost all ~-965 (mover is lost): every / nearly every move loses.
- Game 150456: activation alternates with ply; high when the mover is lost (ply 31,33,35), low when mover has an immediate win (ply 34).
## Hypotheses
H1: fires when the player to move has (almost) no safe move: each legal move either ignores a must-block or plays under an opponent threat cell.
H2: an empty/low column flanked by full columns (deep well) -- likely a correlate of H1.
H3: opponent has 2+ threat cells (stacked threats).

## Dev metric log
- s1 p1 (no immediate win; every legal move lets opponent win at once): F1 0.237 P0.28 R0.21 AUROC 0.595 sim 0.02. FPs: many single-legal-column endgames; misses: early positions.
- facts teacher scores: lost/forced positions are also common in band 1 (50-80th pct), so "lost" is not specific.
- s2 p2 (lostish: double threat / stacked their threats / no safe move): F1 0.14.
- s3 p3 (p1 + >=2 legal columns): F1 0.174, worse; the 1-legal FPs were not the main problem.
- s4 p4 (late ply + 2-3 legal cols + threats): F1 0.185, AUROC 0.617, sim 0.06.
- s5 p5 (opponent threat directly above a landing cell; col2/col4 must-block bonus): F1 0.11, R 0.73, AUROC 0.687 (too broad, fires 37%).
- s6 p6 (combo p4+p5): F1 0.197, AUROC 0.65, sim 0.058.
- s7 p7 (must-block in column 2 OR late combo): F1 0.124.
- s8 p8 (combo with no-safe-move): F1 0.178, sim 0.059.

## Minimal pairs (act)
- 6-stone positions with an opponent must-block on row 0: block at col 2 -> 2.1-2.3 (fires); col 4 -> ~1.1; col 3 -> -0.1 to 0.35; col 5 -> 0.25.
- Opponent vertical three: col 2 -> 1.95; col 4 -> 0.94; col 1 0.57; col 3 -0.67; col 0 -0.76; col 5/6 ~0.
- But the col-2 effect depends on where my stones are (X at 4,5,6 with O col-2 three -> 0.2), and a floating col-2 threat does not fire. My own col-2 win does not fire.
- In games, activation alternates strongly with ply and peaks when the mover is lost late in the game; the same final board reached by different move orders gives 2.9 to 6.0, so move order matters (not a pure board function).
- steer: max/zero changes move probabilities by <= 0.02 on 4 positions (lost positions, already near-uniform policy).

## Conclusion
No clean concept. Best F1 0.237 (p1). Looks like a mixture: late-game lost-position signal plus a column-specific (col 2 > col 4) opponent must-block signal in early positions. Confidence low.
