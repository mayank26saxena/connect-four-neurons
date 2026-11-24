# U32 notebook (layer 3, pole -, threshold 0.906, dev max 10.875)

## Examples
Top bands: nearly all have an opponent (O) stone at (row1, col2) (often X at (0,2) beneath), columns 0 and 1 empty or nearly empty.
Often (0,3)=O too (opponent anti-diagonal (0,3),(1,2) pointing at empty (2,1),(3,0)). Not mirror symmetric (mirror of max pos: 0.34).

## Hypotheses
H1: O at (1,2) and columns 0,1 low (<=1-2 stones).
H2: opponent anti-diagonal (0,3)-(1,2)-(2,1)-(3,0) with >=2 O and rest empty.
H3: something about col 2 stack generally (O stones in col 2 with left side empty).

## Minimal pairs (act), base = 4,6,5,4,3,2,2,2,4,5,4 (10.875)
- col2 X,X,O instead of X,O,X (so (1,2)=X): 0.05.  (1,2)=O variants: 3.3-10.9. => (1,2)=O key.
- Filling col0 to 4: 4.8; col1 to 4: 2.4; both to 4: 0.35. => left side emptiness needed, col1 more.
- Removing (3,4) O: 8.4. First stone (0,4) changed: 0.96.
- Isolated O at (1,2) on a near-empty board (3,2,2,...): ~0. Needs a developed mid-board too.
- Steer: effects small (<=0.16 prob). max-steer on 3,5,1,4,5,2 raises col3 +0.14, lowers col4.

## Dev metric log
- call 1/2 (p1: (1,2)=O and cols 0,1 <=1 stone): F1 0.300 (P 0.23, R 0.43), AUROC 0.69, sim share 0.10. (call 1 and 2 were the same program; I re-ran by mistake.)
- More minimal pairs: on 2,2,5,4,4,4,2,6 (1.73): (2,2)=O instead of X -> -0.40; (2,2) empty -> -0.14; col4 empty -> 0.09; (0,5)=O -> 4.2.
  X at (0,0) kills (0.16), O or X at (0,1) boosts (3.0-4.7). Shifted versions (one column right or left, one row up) do not fire.
- Cell-frequency counts (top >2 vs low): signature (1,2)O, (2,2)X, (1,4)X, (2,4)O, (1,5)X, (0,4)O, (0,5)O; cols 0-1 rows>=1 empty in ~95%.
- call 3 (p2: (1,2)O + count of signature cells): F1 0.370, sim 0.17.
- call 4 (p3: left low AND (A: (1,2)O under (2,2)X  OR  B: (1,4)X under (2,4)O)): F1 0.380 (P 0.35 R 0.42), sim 0.26.
- call 5 (p4: hand-weighted count of signature cells minus bad cells, left low): F1 0.427 (P 0.48 R 0.38), sim 0.33.
- call 6 (p5: p4 with (1,2)O double weight, soft left penalty): F1 0.466 (P 0.46 R 0.47), AUROC 0.73, sim 0.34. BEST.
- ~20% of strong firing has neither A nor B; those show other mixed O/X stacks in cols 2-4 with cols 0-1 empty. Looks like a distributed
  pattern detector over the left-centre (cols 2-5, rows 0-3) gated by empty columns 0-1, not one clean concept.

## Steer
Effects small everywhere (<= 0.16 prob). Max position: zeroing raises col6 +0.16, lowers cols 1,4,5 ~0.04. On 3,5,1,4,5,2 forcing max raises col3 +0.14 / lowers col4 -0.14. Others ~0.

## Synthesis
4,6,5,4,3,2,2,2,4,5,4,6,1 = 12.36 (beats 10.875); 4,6,5,4,3,2,2,2,4,5,4,1,0 = 11.45 (beats); dev max position itself 10.875.
