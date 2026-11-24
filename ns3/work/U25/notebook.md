# U25 notebook (layer 4, pole +, threshold 0.544, dev max 8.53)

## Observations (examples, ~540 positions across bands, seeds 1-3)
- Firing is bimodal in ply: many openings (ply 4-9) and many ply 20-29 positions; rare at ply 30+.
- Not tactical: must-block / immediate-win rates are similar across bands.
- Cell histograms (single cells, by band):
  - early hi: (0,1) mine 59%, (0,3) theirs 57%, (0,2) empty 61%  (lo: ~30%/36%/31%)
  - late hi: (4,2) theirs 76% (lo 34%), (3,2) mine 68%, (2,2) theirs 57%; col 2 top stone often theirs.
- Board-based (transposition 1,3,0,0 == 0,0,1,3 both fire ~3).
- steer: tiny effects (<=0.05 prob), e.g. 1,3,0,0 max: col4 +0.05.

## Hypotheses
- H1: early: my stone (0,1), their stone (0,3), (0,2) empty.
- H2: late: their stone at the top (or at row 4) of column 2.
- H3: unit is a mixture / column-2-centred abstract feature.

## Minimal pairs
- 1,3 base, (a,b) grid at ply 4: fires for 25/49; column-specific (shift to 2,4 -> no; mirror 5,3 -> no).
  Their last stone at col 4 or col 1 tends to kill it; at col 0/6 tends to fire.
- 2,2,2,2,6,2 (O at (4,2) alone) = 0.03: (4,2)=theirs alone is not sufficient.
- seq 3,5,2,1,1,3,3,6,1,5,2,5,5,2,1,1,4,3,6,2 + last move: col2 (O to (4,2)) 4.26, others <0.5.

## Score 1 (p1: col-2 top theirs OR early (0,1)mine/(0,3)theirs/(0,2)empty): F1 0.070, P 0.037, R 0.52, AUROC 0.55, sim share 0.09. Far too broad.

## Late-mode minimal pairs (seq2 = 3,5,2,1,1,3,3,6,1,5,2,5,5,2,1,1,4,3,6,2,2, act 4.26)
- Removing their stone at (4,2) kills (-0.07); removing their (3,5) kills/weakens; removing their (0,4) or (1,6) keeps (3-6).
- Adding any stone to column 3 (height 4 -> 5) kills (~0.3).
- Adding their stone at (2,6) -> 7.46 (on the other diagonal (5,3)-(4,4)-(3,5)-(2,6)).
- Built board with their stones on (2,0),(3,1),(4,2): fires 0.8-2.3 for col-3 heights 0,2,3,4; not for height 1 (with extra their stone at bottom right). Breaking (3,1) to mine -> -0.02.
- Late hi cell histogram: (2,0) theirs 40%/mine 6%, (3,1) 49/26, (4,2) 76/8, (5,3) 44/13.
=> H5: their stones on the up-right diagonal (2,0)-(3,1)-(4,2)-(5,3) with none of mine (and maybe the mirror diagonal (2,6)-(3,5)-(4,4)-(5,3)), i.e. their potential on the top-centre cell (5,3).

## Scores
- s2 p2 (>=2 theirs, none mine, on diagonal (2,0)-(3,1)-(4,2)-(5,3)): F1 0.122 P 0.088 R 0.19 AUROC 0.566, sim 0.09
- s3 p3 (diag with (4,2) theirs, OR early (0,1)mine/(0,3)theirs/(0,2)empty/(0,4) not theirs, ply<=9): F1 0.167 P 0.137 R 0.21 AUROC 0.586, sim 0.09  <- best
- s4 p4 (early-only refined): F1 0.100 P 0.161 R 0.072
- s5 p5 (col2 height>=5 with their (4,2), (3,1) not mine, col3 even): F1 0.090 P 0.06
- s6 p6 (p3 + mirror diagonal (2,6)-(5,3), col3 height<=4): F1 0.114
- s7 p7 (p3 + col3 height<=4): F1 0.132 P 0.138 R 0.127
Nothing tested exceeds 0.17. The unit looks like a mixture: an opening part (their centre-bottom stone with my stone at (0,1) and a gap at (0,2)), and a late part loosely tied to their stones on the left up-right diagonal into (5,3), with many context-dependent exceptions (minimal pairs show single distant stones swinging it by 2-3 units).

## Effect (steer)
Small: forcing it high moves at most ~0.13 of probability, usually toward column 4 (e.g. 3,0,4,5,3,1,4: col3 -0.13, col4 +0.13; others +-0.02-0.05). Zeroing it changes almost nothing.

## Synthesis
seq2 variants with extra their stones at (2,6) and on column 0 ((2,0) theirs) beat the dev max: 12.56, 12.33, 11.67, 11.45.
