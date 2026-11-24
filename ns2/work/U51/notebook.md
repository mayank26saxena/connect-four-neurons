# U51 notebook (layer 5, pole +, threshold 2.760, dev max 9.037)

## Examples
Top firing: column 2 (sometimes 3, 4) is a deep empty/low "well" while neighbours (cols 1 and 3) are tall.
Many have a must-block in column 2 ((1,2),(2,2)).

## Hypotheses
H1: column 2 much lower than both col 1 and col 3 (deep well at col 2).
H2: any interior column (1-5) much lower than both neighbours.
H3: opponent threat in column 2 (their_wins cell in col 2 above landing).

## Score 1 (p1: their threat at landing or landing+1, central weight): F1 0.100, P 0.054, R 0.66, AUROC 0.67, sim -0.02. Bad.
## Minimal pairs (game 3,4,6,2,0,5,3,6,3,3,2,5,2,6,5,6,6,2 + x)
Ply-18 pos: I own threat (2,4) above landing -> 1.2. After opp plays anything but 4: their threat (2,4) sits right above my landing (1,4) -> 4.3-7.8.
After opp plays 4 (threat becomes a must-block at landing) -> 2.67. So: poisoned cell above my landing.
Counterexamples in dev with their threat at row 1 above landing 0 -> low. H4: zugzwang parity -- their threat on a row of THEIR good parity
(first player: row index even; second player: odd).

## Score 2 (p2: opponent good-parity non-playable threat): F1 0.091. Bad; threats too common.
## Pivot
- Vertical opp three (must-block) in cols 0-2 fires early (3-4.5), cols 3-6 do not (asymmetric, odd).
- Horizontal threat above landing early: no.
- Band 9 (14/14 checked): teacher scores say EVERY legal move loses (~-97x); model output ~uniform.
- Early forced losses (open three on row 0) give 1.3-2.9 (sub/near threshold): lost + later in game = higher.
H6: unit = "side to move is lost". Program p3: bitboard search depth 7 (forced moves pruned), lost => fire.

## Score 3 (p3: side to move lost by depth-7 search): F1 0.194 (P 0.135, R 0.347), AUROC 0.64, sim 0.00. 1218 s (slow!).
FPs: lost positions where I ALSO own many threat cells (act -4.9, -3.4). Misses: opponent threat directly above a landing
cell with no/few threats of mine (engine often lost, search can't see the zugzwang).
H8: opponent has a "poisoned" column (their threat directly above my landing cell) and I have no threat cells.
## Score 4 (p4: poisoned column + no threats of mine): F1 0.080. Dead end.
Next p5: p3 lost-search but only when I own at most one threat cell.
## Score 5 (p5: lost by search AND I own <=1 threat cell): F1 0.200 (P 0.171, R 0.240), AUROC 0.60, sim 0.00. Best, still weak.
Steer: near zero in lost positions (<0.03); forcing max in normal positions adds +0.02-0.08 to the already-preferred column.
Synthesis: greedy 2-ply search from a dev top position reached 9.469 (beats dev max 9.037).
Conclusion: unit correlates with "side to move is lost, opponent holds threats, I have no counterplay" but no board rule
reaches F1 > 0.2. Confidence low. Stopped at 5 score calls.
