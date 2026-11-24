# U29 notebook (layer 5, pole -, threshold 1.565, dev max 10.39)

## Observations (examples, bands 0-9)
- Fires on alternating plies within a game: tied to the side to move (me-stones config).
- Top examples: column 3 is almost always full or has a threat cell directly above its landing cell; model gives col 3 ~0 prob.
- Many firing boards have deep "wells" (empty/low columns beside tall ones), often cols 1,2,5.
- Steer: effect tiny (<=0.04), slightly lowers col 3 when forced max.

## Hypotheses
H1: some landing cell has my threat directly above. Minimal pair: my threat (1,3) above empty col3 fires 5.5; same threat cells at (1,0),(1,4) above empty landings: -0.23. Rejected as general.
H2: col 3 full -> no (3x6 stack openings ~ -0.5).
H3: col 3 full or col 3 landing poisoned (threat above landing).

## Score calls
1. p1 (col3 full or threat directly above col3 landing): F1 0.087 (P .047 R .717), AUROC .62, sim -0.02. Col3-full is common; rejected.
2. p2 (any legal column with a threat cell, either side, directly above its landing): F1 0.074, program fires 54%. Rejected.
3. p3 (hand-picked cells from single-cell histograms: mine at (1,2),(1,3),(2,1),(3,2),(3,3),(4,4); theirs at (2,3),(4,3),(3,1),(3,4),(1,1); col5 height<=1; >=8 of 12): F1 0.173 (P .145 R .213), AUROC .59, sim -0.08.
4. p4 = p3 + column-height parity terms (col2 even, col1 odd, col5 odd): F1 0.176, AUROC .59, sim -0.08. Best, but marginal.
5. p5 = p3 cells + "poisoned column" count, no immediate tactics: F1 0.158.

## Minimal pairs (act)
- 3377 family (4,2,4,1,2,2,0,5 = 2.5): needs BOTH X(0,0) and O(0,5); moving either to col 6 drops to <0.5. Distant-cell interaction.
- Fires on alternate plies within a game (side-to-move specific).
- 62998 family: anything that puts a stone at (3,5) (under their threat (4,5)) kills it (8.8 -> ~0-1); other columns keep it 5-8.
- 14515: filling (3,1) under my threat (4,1) or raising col5 1->2 kills; but constructed clean "threat above landing" positions do NOT fire (-0.2, 0.1, 0.9).
- Col 3 filled early (3x6): no firing.
- Histograms: band 9 skews me_first (66%), col5 low, col2 even height, col3 full; no single feature separates.

## Conclusion
No clean board concept found; activation depends on interactions between distant cells and column parities. Looks like a distributed/polysemantic or random direction. Confidence low.
Steer: forcing max/zero changes move probabilities by <=0.04 (slight drop of col 3).
Synthesis: 62998 line extended (..,6,0,6,0) reaches 10.62 > dev max 10.39.
