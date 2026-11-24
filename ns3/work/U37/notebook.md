# U37 notebook (layer 5, pole -, threshold 1.133, dev max 4.618)

## Observations (examples, bands 0-9)
- Top firing: late-game boards (ply 22-32) with most columns tall/full and one or two empty / near-empty columns
  (often columns where the cell above the landing cell is a threat cell -> suicidal column). Exception: 75818 (ply 7, fires 1.83).
- act: 4,2,5,5,2,6,X fires only for X=0 (1.83); other last moves ~0. Very order/position sensitive.
- 148571: last move 0 (blocking) -> 3.2; other columns at that ply ~ -0.3; ply 25 was -5.9 (must-block position).
- 6855: ply 30 fires only if last move fills col 6 (leaving cols 0 and 3 empty, everything else full); alt 0 -> 0.63, alt 3 -> 0.11.
- Pure shafts on empty boards (2,2,4,4,...) do not fire; col 0 at height 5 alone does not fire; horizontal OOO over empty col 3 does not fire.
- steer (4 positions): forcing the unit high raises column 0 by ~+0.02..+0.08, zeroing lowers column 0 by ~0.07-0.09. Small effect.

## Hypotheses
H1 poisoned column (cell above landing is a threat): fails minimal pair on sparse board; band 1 has counterexamples.
H2 both sides have threat cells in the same column: near-threshold non-firing counterexamples.
H3 late-game "wells": a column of height <=1 while several columns are full / >=5 tall.
H4 column 0 is the move the model likes (effect is +col 0).

## Score log
- s1 p1 (height spread: a column h<=1 and >=3 columns h>=5): F1 0.136 P .076 R .663 AUROC .70, sim -18.9. Too broad.
- s2 p2 (<=4 legal, col 0 legal, no immediate wins): F1 0.233, AUROC .72, sim negative.
- Histograms by band: col 0 height 5 in 52/74 band-9 samples vs 2/90 band-1; col 0 full never appears above band 0
  (full col 0 drives pole strongly negative, e.g. -17 right after col 0 fills).
- s3 p3 (col 0 height == 5): F1 0.253 P .19 R .385 AUROC .665, sim share 0.23.
- s4 p4 (col0 h5 & >=2 full cols, or col0 h<=1 & >=3 full; no immediate wins): F1 0.326 P .25 R .48, sim share 0.29.
- s5 p5 (+ "poisoned column" term): F1 0.159; poisoned columns are far too common. Dropped.
- s6 p6 (additive score: col0 h5, >=3 tall cols, 1-2 low cols, ply 22-35): F1 0.287, sim negative.
- s7 p7 (p4 + last stone landed in rows 4-5 with >=2 full cols): F1 0.247 (recall .63, precision .15), AUROC .756, sim 0.27.
- Best = p4 (F1 0.326, sim share 0.29). Final.

## Minimal pairs supporting the col-0 story
- 24634: ply 24, O drops into col 0 making it height 5 -> 2.45; same ply other moves -0.6..1.2; next move fills col 0 -> -16.9.
- dev-max game: sibling last move that fills col 0 -> -5.3, others 0.6-4.6.
- But toy positions (0,0,0,0,0,x ...) are erratic: col 0 height 5 alone is not sufficient. Many top boards instead have col 0 empty
  with most other columns full (6855). Order/parity sensitive; no clean rule found.

## Effect (steer, 5 positions): forcing high raises col 0 by +0.02..+0.08; zeroing lowers col 0 by 0.07-0.11 (to cols 1/5). Small.
## Synthesis: hill-climbed single-move substitutions of the dev-max game -> 4.837, 4.796, 4.780, 4.710, 4.650 (all beat 4.618).
