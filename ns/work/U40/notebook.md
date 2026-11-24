# U40 notebook (layer 2, pole +, thr 0.638, dev max 5.663)

## Observations
- Top band (2.5-3.0) is dominated by ply-3 openings (me = second player, one X vs two O, all on bottom row), e.g. 3,2,4 / 6,2,4 / 4,2,6.
- Sampled firing positions: ~half are ply 3, the rest spread over ply 19-40 with no obvious shared tactic.
- Activation oscillates with parity in a game: higher right after the first player moves (me = second player).
- Swept all 343 ply-3 openings with act (ply3.txt): 117 fire. Never fires when my stone is in col 3 (except a few with O at 3 also).
  Rarely fires when the first move was col 0 or col 5. Strong for my stone at col 2/4/6 etc.
- steer to zero: changes move probs by <= 0.04; tiny effect.

## Hypotheses
H1: ply 3 and my single stone is not in the centre column.
H2: late game: unclear (edge columns empty / centre full?).
H3: random direction / mixture (asymmetric ply-3 table suggests a non-semantic direction).

## Score calls
1. h1 (ply 3, my stone not in col 3): F1 0.424 P 0.544 R 0.348 AUROC 0.669, sim share 0.04. Ply-3 openings ~35% of firing.
2. h2 (+ late: col 5 full, col 0 <=3, no my win): F1 0.196. Col-5-full rule far too broad. Dropped.
3. h3 (opening refined: my stone not col 3/5, col 5 empty; late: their stone at (4,5)): F1 0.238 P 0.146 R 0.650 AUROC 0.764.
   Per-cell counts (firing vs non, ply>=12) showed (4,5) theirs 84% vs 11%, (4,4) mine 64% vs 22%, (5,5) theirs, (3,5)/(2,5) mine.
4. h4 (opening OR >=6 of 9 cell conditions): F1 0.462 P 0.397 R 0.552.
5. h5 (opening OR [(4,5) theirs, (4,4) mine, and (5,5) theirs or (3,5) mine] with >=5 points): F1 0.480 P 0.445 R 0.520 AUROC 0.75, sim share 0.09. BEST.

## Minimal pairs
- 101562 ply-23 prefix + any opponent move fires except col 4 (which puts their stone on (4,4)): consistent with (4,4)-mine.
- 20769: their stone landing on (5,5) gives 2.41 vs ~1 for other moves: consistent with (5,5)-theirs.
- BUT building the col-5 pattern (mine at rows 2-3, theirs at rows 4-5) on an otherwise empty board gives -1.2 to -0.8. So the
  late cell pattern is a correlate within particular game lines, not a sufficient cause. Unit looks like a distributed /
  possibly random direction. Ply-3 table (ply3.txt) is asymmetric (col 5 for either player suppresses, my col 3 suppresses).

## Steer
Zero and max on 4 positions: all move-probability changes <= 0.05. Effect: none measurable.

## Synthesis
Greedy 2-ply hill climb from dev pos 101562: best 5.090 at ply 30 (below dev max 5.663). A ply-32 5.26 line was discarded
because it passed through a completed four for me.

## Audit fix (orchestrator, before verification)
The two ply-30 synthesis lines (...,4,5,2,6,2,3 = 5.090 and ...,4,5,2,3,2,6 = 5.080) complete a four at move 29, so they are invalid.
I wrote checkwin.py (it reports the first move that completes a four) and ext.sh (2-move extensions that skip any line where a move completes a four).
Replaced them with B+2,6 (synth 4.615) and B+2,3 (synth 4.601), where B = the ply-26 line (3.369). Extending those by 2 more moves without completing a four gave at most 4.44.
Kept B, 3,2,4 (2.970) and 6,2,4 (2.949); checked that none complete a four. No score calls used. Only the synthesis and notes fields changed.
