# U31 notebook (layer 1, pole -, threshold 1.833, dev max 5.538)

## Examples (60+ looked at)
- Band 9: all are "last move = col 2, landing on row 0", early game (ply 4-10).
- Band 5-8: nearly every firing board has column 2 with exactly one stone, the opponent's (O) at the bottom, even when the last move was elsewhere.
- Lower bands: col 2 empty, or mine at the bottom, or taller.

Hypotheses:
H1: fires when cell (0,2) is theirs and (1,2) empty (col 2 height 1, opponent stone).
H2: strongest when that stone was the just-played move; decays with ply / other moves.
H3 (alt): any last move on bottom row -> rejected by act (6,5,6,1 / 6,5,6,3 / 6,5,6,4 / 6,5,6,0 all < 0.7).

## Minimal pairs (act)
- 6,5,6,2 = 5.30 ; 6,5,6,2,2 (col2 height 2) = 0.35 ; 6,5,2,6 (col2 bottom is MINE) = 0.30
- 6,5,6,{0,1,3,4} = 0.2-0.7 (only col 2 matters)
- 2,5,6,6 (bottom col2 mine) 0.27 ; 2,5,6,6,0 (same stone now theirs) 2.06 FIRES
- 6,5,6,2,0 = 1.87, 6,5,6,2,0,1 = 2.79, 6,5,6,2,3,3 = 2.49: still fires when other moves follow, weaker
- 3,3,3,3,2 = 2.97 ; 0,2,0,3 = 1.97 ; 4,4,2,4 (mine) 0.60
=> H1 holds; H2 holds (last-move bonus).

## score 1 (p1: (0,2) theirs and (1,2) empty): F1 0.441 P 0.295 R 0.873 AUROC 0.905; sim share 0.58
Too broad. Misses include col-2 single stone that is MINE at low ply (2,0,5,1,1,3 = 2.10).
More act:
- ply decay with last move col2 bottom: ply4 ~5, ply11-12 1.6-2.2, ply13 1.3-1.4, ply17-18 ~0.55.
- ownership matters some (theirs +0.5..0.8 at matched games: 2,0,5,1 1.10 vs 2,0,5,1,1 1.84; 0,0,2,0 1.15 vs 0,0,2,0,0 1.90) but mine can still fire early.
- neighbors: 6,2,6,X gives 1.05-2.31 depending on X; 2,5,6,6 only 0.27. No clean neighbor rule.
=> H4: col 2 has exactly one stone, and the game is early (ply small); last move into col 2 extends the ply range.

## score 2 (p2: col2 height 1 + ply cutoffs): F1 0.534 P 0.407 R 0.775 AUROC 0.871; sim share 0.67
Key act finding: at ply 4 EVERY "opponent just dropped into empty col 2" fires (2.7-5.3: 4,1,4,2 2.70, 3,3,3,2 4.03, ...),
while non-last single-stone col2 at ply 4 does not (4,2,4,X 0.86-1.62). Last move into col 2 at row>=1 never fires (0.15-0.36).
Decay is not just ply: tall columns depress it. Ply13 flat board (all heights 2) 2.75; ply13 with two full columns 0.9-1.2; ply19 flat (heights 3) 1.33.
Hand model from these pairs: est = 4.5 - 0.15*(ply-4) - 0.2*(stones in rows >= 2). Residual (col2 single stone, not last move) ~ est - 2.

## score 3 (p3: linear est with tall-column penalty, residual = est-2 (+0.4 if theirs)): F1 0.539 P 0.410 R 0.786 AUROC 0.876; sim 0.60
Barely better than p2 in F1, worse simulation. Residual (col2 single stone not just played) is the noisy part.
Act: residual is board-dependent, not move-order dependent (4 orders of the same board 2.06-2.19). Ownership matters in residual
(6,4,2,6 mine 0.14; 2,5,6,6,0,1 mine 1.31 vs 6,5,6,2,0,1 theirs 2.79), but mine flanked by opponent bottom stones can fire (2,0,5,1,1,3 2.10).
Band-6 non-last-col-2 firing (21 boards): all have col 2 with exactly one stone; 18/21 theirs; ply 5-11; mostly flat.

## score 4 (p4: residual theirs = est-1.4, mine = est-2.6): F1 0.606 P 0.511 R 0.744 AUROC 0.861; sim 0.60
Misses shown are late-game (ply 18-27) "just dropped into col 2 bottom" boards with full bottom rows; my ply penalty too harsh there.
Act: filling the bottom row RAISES it (3s4s+2 0.91 -> +6,1,5,0 then 2: 1.67); stones in row 1 and above lower it.
Rough per-row weights (saturating, not linear): row0 ~0, row1 ~-0.3, rows>=2 ~-0.25 per stone.
p5: est_last = 4.8 - 0.3*n_row1 - 0.25*n_rows>=2 (bottom-row stones free).

## score 5 (p5): F1 0.618 P 0.514 R 0.772 AUROC 0.875; sim 0.62
Remaining errors are mostly residual cases near threshold. Act pattern: residual with MY stone in col 2 is low at ply 4
(2,5,6,6 0.27; 6,4,2,6 0.14; 2,0,5,1 1.10) but ~2 at ply 6-7 (2,0,5,1,1,3 2.10; misses 6566, 21233). p6: penalise residual at ply 4-5,
soften mine penalty after; also floor level of just-played col-2 cases (p2 had higher levels and better simulation).

## score 6 (p6): F1 0.603 P 0.487 R 0.793 AUROC 0.884; sim 0.63. Not better on F1; keep p5 as final program.

## steer
- 6,5,6,2 (act 5.3): max no change; zero: col2 -4 pts, col4 +2.
- 3,3,3,3,2: max col4 +4 / col1 -4; zero col1 +5 / col4 -5.
- 6,5,6,1 (not firing): max: <=2 pts.
- flat ply-13 + 2: max col4 +2 col6 -3; zero col6 +4 col4 -3.
=> Effect small (<=5 pts) and position-specific; no consistent column push.

## synthesis
Brute-forced all ply-4 "a,b,c,2" (no col 2 earlier): best 3,5,6,2 = 5.538 (= dev max), 6,5,3,2 5.534. Opponent stones on the right half help.
Extended: 6,5,3,5,6,2 = 5.681 (beats), 3,5,6,5,3,2 = 5.577 (beats); 3,5,6,2 / 6,5,3,3,6,2 / 6,5,3,2 tie or just below.

## Final: p5 (F1 0.618, P 0.514, R 0.772, AUROC 0.875, sim share 0.62). Confidence medium (F1 in 0.4-0.7; residual part noisy).
