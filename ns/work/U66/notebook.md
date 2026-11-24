# U66 notebook (layer 2, pole -, threshold 0.422, dev max 4.143)

## Examples (60 viewed)
Top band dominated by: last move in column 6, with O (opponent) stones at the top of column 6, often 2-3 stacked O (vertical threat at col 6).
Some top ones have last col 0 (45450: 6,4,2,2,4,0 = 4.06, col 6 just my X at bottom).

Hypotheses:
- H1: top stone of column 6 is the opponent's, especially just played (last_col==6), stronger with more O stacked.
- H2: opponent has stones on the right edge / vertical stack in col 6 (threat at col 6).
- H3: something about last move at edge columns (0 or 6).

## Tests (act minimal pairs)
- Every single-move substitution in 6,4,2,2,4,0 (4.06) lowers it, but most variants still fire: dense, distributed response.
- Stones added to column 4 beyond height 2 kill it (4,6,4,6 0.97 -> +4,4 -0.77). Col4 height 1-2 strongly enriched in top bands (histogram).
- Grid of adding (X at a, O at b) to 4,4,0: O wanted in cols 0,2,6, not 1,3,5; anything in col 4 kills.
- Two O stones on bottom row: O at cols 4 and 0 best (1.23); move order matters a little (4 then 0 > 0 then 4).
- Vertical O three in col 6 alone does not fire (6,0,6,0,6 0.13) but does with my stones in col 4 (6,4,6,4,6 1.31).
- Same board via different move orders: 3.0-4.06, last move into col 0 better than col 2. Mostly board-determined.
- Histograms: last move col odd (1,3,5) rarely fires; cols 1 and 5 empty enriched; col6 top O-O(-O) enriched in band 9.

## Dev metric
1. p1 last_col==6 & h4 in 1..4: F1 0.168, AUROC 0.59, sim 0.06
2. p2 points (h1,h5 empty, h4==2, O even/odd cols, last col even): F1 0.221, sim 0.06
3. p3 tighter template: F1 0.148 (prec 0.36, rec 0.09), sim 0.09
4. p4 points incl. col6 stack, ply penalty: F1 0.201, sim 0.09
5. p5 last col + h4 + bits: F1 0.205, sim 0.10
6. p6 + odd cols empty + my previous move central: F1 0.228 (prec .37 rec .17), sim 0.12
7. p7 = p6 with lower threshold 4.0: F1 0.286 (prec .215 rec .429), AUROC 0.689, sim 0.12  <- final

No rule exceeds 0.3. Activation looks like a dense board template (opening family with O on bottom of cols 0/4, col4 height 1-2, odd columns empty, opponent's last move in col 6/0, often O stack in col 6), not a clean concept. Confidence low; possibly a random direction.

## Steer
Max/zero steering on 4 positions: changes <= 0.03 in any column. Effect none measurable.

## Synthesis
3,2,4,6,2,4,2,4,6,3,6 = 5.53 (beats dev max 4.143); 3,2,4,6,6,4,2,4,2,3,6 = 5.51; 3,2,4,6,6,4,2,4,6,3,6 = 5.11; 3,2,4,6,6,4,2,4,6,5,6 = 4.15; 6,4,2,2,4,0 = 4.06.
