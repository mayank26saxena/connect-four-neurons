# U18 notebook (layer 0, pole -, threshold 2.886, dev max 10.26)

## Examples (40, all bands)
Every firing example (bands 5-9) has last move in column 4, and that stone landed on the bottom row (column 4 was empty).
Band-4 near misses: last move col 4 but on row 1 (acts 1.5-2.5). Top band = early positions (ply 4-9).

Hypotheses:
H1: fires iff opponent's last stone was dropped into an empty column 4 (lands at row 0). Strength falls with ply.
H2: any last move in col 4 (row irrelevant) -- contradicted by examples with row 1.
H3: something about col 4 contents/neighbours -- check via act.

## act minimal pairs
- 2,3,1,4 -> 8.82 FIRES; +4 (row1, me) -0.45; +4 (row2) -3.66
- 0,0,0,4 6.37 F; 3,3,3,4 7.26 F; 3,3,3,3,4 5.62 F; 1x6,4 (ply7) 3.42 F; 6x6,0x6,4 (ply13) 3.12 F
- 0,0,4,4 (col4 row1) -0.88; 3,4,3,4 (row1) 2.33; 0,0,4,0,4 (row1) 1.98; 4,4,4,4,4 -10.4
- 2,3,1,{3,5,0} -> -0.4,-0.4,0.87 (other columns no)
=> H1 supported. Activation decreases with ply and with neighbouring stones? (ply 4: 7-8.8)

## score 1 (p1: last col 4 at row 0): F1 0.800, P 1.00, R 0.666, AUROC 0.833, sim share 0.53
Misses: last move col 4 at row 1 stacked on the opponent's OWN earlier stone in col 4, in longer games.
act tests: row-1-on-own at ply 4-8 ~2.0-2.6 (just below), ply 12 2.8-3.3, ply 16-28 3.6-6.4 FIRES.
Row 1 on my stone (X below): -0.9..2.1 even at ply 26 -> no. Third col-4 stone by same player -> no.
Neighbouring column heights: no effect. Interpretation (layer 0): "opponent dropped into col 4 and col 4
has none of my stones and at most one earlier stone of theirs; earlier col-4 stone matters less in long games".
H1b: fires if last col 4 and (row 0, or row 1 on their own stone and ply >= 12).

## score 2 (p2: row0, or row1 on own stone with ply>=12): F1 0.903 P 0.984 R 0.834 AUROC 0.917 sim share 0.55
Misses mostly row-1-on-own at ply 6-10 (acts 3.0-4.1); also an odd row-1-on-my-stone at ply 23 (3.36), rare.
act: row-1-on-own at ply 8-10 is borderline (2.8-4.1, depends on other moves).
## score 3 (p3: same, ply>=8): F1 0.943 P 0.968 R 0.920 AUROC 0.959 sim share 0.55  <- best

## steer (3 positions)
2,3,1,4: zero -> col3 -4, col4 +5; max -> ~+1 col3. 3,3,3,4: zero -> col3 -5, col4 +3. 0,3,0,5,6,3,5,3,3,0,4: zero -> col3 -9, col2 +9.
Effect: when active it pushes the move toward column 3 (next to the new col-4 stone) and slightly away from stacking col 4; small (a few points).

## Top band / synthesis
Top dev examples include ply-15 games (9.58), so strength is not just early ply: earlier moves in columns 0-1 raise it, moves in 5-6 lower it.
Found 6,2,2,5,3,2,1,3,3,6,3,3,5,0,1,1,0,0,4 = 10.80 (beats dev max 10.26).
## score 4 (p4: same fires, flatter level): F1 0.943, sim share 0.55 (unchanged). Level shape barely matters; stopping.
Final = p4 (same detector as p3).
