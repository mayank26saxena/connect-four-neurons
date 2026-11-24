# U02 notebook (layer 5, pole -, threshold 3.996, dev max 12.789)

## Observations from examples (bands 0-9, ~200 positions)
- Firing is purely late-game: ply 26-41, many full columns.
- Per-band counts of full columns: col 0 and col 3 full in 40/40 band-9, 36/40 band-7, 32/40 band-5, 25/40 band-4, 14/40 band-3.
- Column 5 is NEVER full in band 9 (0/40) and often empty/height<=1 (24/40).
- Model's move distribution is near-uniform in some firing positions.

## Hypotheses
H1: "board nearly full" (ply / count of full columns). Partially true but band 3-4 also have many full columns.
H2: specific columns full: col 0 AND col 3 full (plus more full columns: 2,4,6), with column 5 (and 1) still open.
H3: parity/zugzwang (which player is to move with threats stacked in open columns). Act traces oscillate by ply.

## Minimal pairs (act)
- toy stacks: F0+F3 = 2.4; F0 alone -0.46; F3 alone 0.7; F0+F2 0.15; F6+F3 1.15. => 0 and 3 jointly.
- F0,F3,F2,F6 = 5.46 vs mirror F6,F3,F4,F0 = 3.14 (not mirror symmetric).
- F0,F3,F2,F6,F4 = 8.53; col4 at height 5 -> 5.8; col0 at height 5 -> 0.88 (!); col3 at height 5 -> 2.19.
- adding a single stone in col 5 or 1 to the 8.53 position: 2.8 / 3.1; two stones in 1: 6.1. Parity of who is to move matters.

## dev call 1 (p1: col0&col3 full and >=4 full columns): F1 0.424 (P 0.31, R 0.69), AUROC 0.82, sim share 0.43
Misses include col3 empty or col0 h5; FPs with 6 full columns and act ~0. Column story is a correlate.

## New lead: parity minimal pairs on pos 72695 (B, 9.12, me=first, cols 1 and 5 open h1)
B 9.12 | B,1 -0.06 | B,5 2.57 | B,1,1 6.86 | B,5,5 5.62 | B,1,5 4.98 | B,1,1,1 0.56 | B,1,1,1,1 4.95
facts: fires exactly when one of MY landing cells has THEIR threat cell directly above it (playing there hands them a win).
H4: "poisoned move": a legal column whose landing cell is directly below an opponent win cell.
Steer (to max): small; raises column 4 by +2..+24 points in 4 positions, lowers 3/5 a bit.

## dev call 2 (p2: any poisoned move): F1 0.115 (P 0.06, R 0.79). Poisoned moves are common midgame; necessary-ish but far from sufficient.
Histograms by band (60 each): #poisoned>=1 in 59/60 band-9, 54/60 band-7, 44/60 band-5, 42/60 band-4, 35/60 band-3, 27/60 band-2.
## dev call 3 (p3: poisoned and >=4 full columns): F1 0.274 (P 0.18, R 0.57). FPs have col 0 or col 3 OPEN -> column identity is real, not just fullness.
## act on pos 24638 (8.61; cols 1,4,5,6 open): filling 4 and/or 6 keeps it high (4.1-8.7); giving ME an immediate win (,1 or ,5) drops to ~2.3.

## dev call 4 (p4: col0&col3 full, >=4 full, >=1 poisoned, no immediate win for me): F1 0.492 (P 0.47, R 0.51), sim share 0.35
Teacher scores on FPs/misses of calls 1,3,4: low-activation late positions almost always have a WINNING move for me (+960);
firing ones mostly have every move losing (-96x) or drawn (0). => unit looks like "late endgame where I have no winning move" (value-like).
Poisoned columns are a proxy for "I am in zugzwang/lost".
act on pos 14861 (FP 1.69, two poisoned columns but col4 wins for me): values 0.5-4 with filling; consistent with value story, not with poisoned count.
## dev call 5 (p5: base & no immediate win & (poisoned or 1 legal or I have no threats)): F1 0.492 (P 0.41, R 0.61), AUROC 0.79, sim 0.35
Misses now mostly have only 3 full columns (col0, col3 + one more) -> relax nfull to >=3.
## dev call 6 (p6: same as p5 but >=3 full columns): F1 0.517 (P 0.40, R 0.72), AUROC 0.84, sim 0.35. Best so far.
Remaining misses are mostly near threshold (4.1-4.6); FPs 1.7-3.7 (also near). Next: test whether the poisoned/threat clause helps at all (drop it, keep "no immediate win"), and a better level.
## dev call 7 (p7: col0&col3 full, >=3 full, no immediate win; no poisoned clause): F1 0.492 (P 0.35, R 0.81), AUROC 0.88, sim 0.36.
The poisoned/threat clause buys precision (+0.05) at a recall cost; p6 remains best F1.
Final = p6 fires + p7-style graded level (full columns + 2 per poisoned move, bonus when every legal move is poisoned, penalty for immediate win).
## dev call 8 (final.py = p6 fires + graded level): F1 0.517 (P 0.40, R 0.72), AUROC 0.84, sim recovers 31.8% (share of ceiling 0.36).
## Synthesis: random/hill search (160 act calls) + hand toys. Best valid 10.46 (dev game 159394), toy full-column stacks 0,3,4,6,2 = 9.32. None beat dev max 12.79.
## Effect (steer): small. Forcing max raises column 4 by +2 to +24 points (largest on an early opening), lowers 3/5 slightly; zeroing it in firing positions changes probabilities by <=5 points.
## Conclusion: medium confidence. Late-endgame detector keyed to columns 0 and 3 being full, strongest when I have no winning move (zugzwang: legal moves sit under their threats). Strong ply-parity sensitivity not fully captured.
