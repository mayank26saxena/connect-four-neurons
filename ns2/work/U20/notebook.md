# U20 notebook (layer 5, pole -, threshold 2.794, dev max 9.405)

## Observations (examples, ~40 + 60/band histograms)
- Top bands are late-game (mean ply ~30 in band 9 vs 15-21 in bands 0-1).
- Column heights by band: col 4 full in 100% of band 9 (10% band 0), col 5 full 97%; col 1 NEVER full in bands 5-9; col 2 rarely full.
- Engine eval: band 9 is ~14/15 lost for the side to move; band 5-7 ~half lost.
- Top examples often contain a column where the opponent's win cell is directly above the landing cell (and often my win cell above that).

## Hypotheses
- H1: right-centre columns (4,5) full, column 1 (and 2) still open, late game.
- H2: "poisoned column": an opponent win cell directly above a landing cell (I cannot play there), in a crowded board.
- H3: side to move is lost (zugzwang endgame).

## act tests
- Only cols 4,5 filled (4x6,5x6, then 0/6): peaks 2.79, not firing; filling col 2 drops to 0.47. H1 alone insufficient.
- Early poisoned column (4,4,5,5,0,6,1,6; their threat (1,3) over landing (0,3)): -0.17 vs 0.44 without. H2 alone insufficient early.
- 97688 prefix P (heights [2,5,5,1,6,5,4], col 3 their (2,3) over landing, my (3,3)): opponent's last move 5 -> 8.99, 6 -> 6.95, 3 -> 5.74, 0 -> 1.86, 1 (fills col1) -> 1.67, 2 (fills col2) -> 0.82. All lost. Filling col 1/2 kills it, filling the right side boosts.
## steer
- 97688: on vs off: col1 +0.05, col2 -0.05. 101829: col1 +0.07/-0.03, col2 -0.06/+0.03. 68489: col1 +0.02. Early must-block positions: no change. Effect small: nudges toward column 1, away from column 2.

## Dev metric log
1. p1 poisoned column (their win directly above a landing cell), ply>=18: F1 0.102 (P .056 R .557), AUROC .634, sim -0.07. Poisoned columns are far too common. Dropped.
2. p2 col 4 full AND opponent has a parity-correct threat: F1 0.203 (P .126 R .52), AUROC .705, sim 0.09. Threat proxy hurts.
3. p3 (h4==6 & h5==6 & h1<6 & h2<6) OR opponent vertical three in col 3/4/5 with must-block on top: F1 0.439 (P .376 R .527), AUROC .750, sim 0.16.
4. p4 col 4 full & opponent controls more columns (lowest threat in column is theirs): F1 0.172. Threat/evaluation proxies do not work; the unit is better read from heights.
5. p5 = p3 with (h5==6 or h3==6): F1 0.401 (P .282 R .693), AUROC .819. h3 alternative adds FPs.
6. p6 = p5 late clause only (no vertical clause): F1 0.354 (P .282 R .475) -> the vertical-three clause carries ~0.22 recall.
7. p7 late = h4==6 & h5+h6>=10 & h1,h2 open; vertical only cols 4,5 (act: col-3 vertical three gives -2.7): F1 0.439 (P .452 R .427), AUROC .706, sim 0.15.
8. p8 late = h4==6 & (h5==6 or h5+h6>=10) & h1,h2 open, OR vertical three in col 4/5: F1 0.493 (P .441 R .559), AUROC .769, sim 0.15. BEST.

## Interpretation
- Unit is mostly an endgame feature: column 4 (and the right side, 5/6) full while columns 1 and 2 still have room. Strongest when the side to move is lost (band 9 14/15 lost per engine), but simple threat proxies for "lost" did not help.
- Smaller early-game component: opponent's vertical three in column 4 or 5 that must be blocked on top (act ~2.5-4, near threshold).
- Strong context dependence: same heights can give 1-9 depending on the last move; e.g. 54893 at ply 30 -0.38, one more opponent stone in col 2 -> 4.29. So the description is a coarse proxy; medium confidence at best.

## Synthesis
- 2-ply search from dev example (8.554): P+0,0 = 9.685 BEATS the dev max (9.405). Several deeper candidates (9.45) were rejected because they complete a four.
## Final: p8, confidence medium (F1 0.493).
