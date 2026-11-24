# U14 notebook (layer 5, pole -, threshold 0.738, max 47.5)

## Examples
- Bands 7-9 (act > 4.4): essentially all = opponent's last move col 1 making three stacked vertically in column 1, cell above empty (must-block in col 1).
- Bands 5-6 (0.74-4.4): mixed; many must-blocks in col 1 (incl. horizontal/diagonal ones), some must-blocks in other cols (5,6,2), some with no threat at all.

## Hypotheses
H1: opponent has a vertical three on top of column 1 with empty cell above (vertical must-block in col 1).
H2: any opponent playable win (must-block) in column 1.
H3: diffuse low part = any must-block / random.

## act tests
- vertical three of theirs per column (d,c,e,c,d,c): col1 20.7, others <0.6. Column-1 specific.
- their col-1 three persists when last move elsewhere (4,1,6,1,4,1,6,0): 11.5 fires. So not strictly last-move.
- my own col-1 three (1,4,1,5,1,6): -1.4. Only opponent's three.
- Horizontal threat at (0,1) (5,2,6,3,0,4): 0.40, not firing.
- vertical threes of theirs in col0/5/6 first player: ~0.
- odd: full column 1 O,O,X,O,X,O (4,1,4,1,1,6,1,6,1,0,1): 6.0 fires.

## Scores
- s1 (vert1 OR any must-block in col 1): F1 0.515 P 0.59 R 0.457. FPs = horizontal col-1 must-blocks where last move was elsewhere.
- s2 (vert1 only): F1 0.427 P 0.994 R 0.272. FPs late full boards only.

## New insight (act trajectories)
13365 / 136171: act jumps from ~-1 to ~2 exactly when opponent drops a stone in col 1 that makes the cell DIRECTLY ABOVE it a winning cell for them (diagonal threat through (1,1)). Horizontal (0,1) threats from moves elsewhere don't fire.
H4: opponent's last stone in col 1 with the cell right above it completing four for them (vertical 3 is the strongest case).
Weak low-band examples in cols 5,6,2,0 look the same (threat directly above opponent's last stone) -> H5 generalises to any column.
- s3 (vert1 OR last stone in col 1 with cell directly above completing four for them): F1 0.513 P 0.705 R 0.404. FPs late game (ply 30+).
- s4 (vert1 OR diagonal-only col-1 must-block): F1 0.482. Worse; miss 5635 (12.4) is horizontal threat directly above last stone in col 1 -> "above last stone" is the right condition, not line direction.
- s5 (s3 with ply<=30 on the second branch): F1 0.488 P 0.828 R 0.346. Worse F1.
- Band 5 (97-98 pct) last-move-column histogram is ~uniform: lower third of firing is diffuse, not captured. Ceiling for a clean rule ~0.5.
- 529 (3.1): horizontal threat at (1,1) with col 1 empty; minimal-pair rebuild (2,2,3,3,4,4,6,0) gives 0.09 -> idiosyncratic.
- Simulation: perfect reader ceiling is negative (-141%), share nan; not informative.

## Steer
- 2,1,5,2,3,4,4,0 max: col1 0.03 -> 1.00.
- 2,0,6,3,0,5,3,0,2,2,4 max: col1 0 -> 0.14 (even though col 1 is losing there). zero: no change.
- vertical-three positions: col 1 already 1.0, no change.
Effect: pushes the model to play column 1 (block).

## Synthesis
4,2,2,3,1,4,1,6,1 = 49.33 (beats 47.52); 4,2,2,3,1,4,1,5,1 = 48.95; 4,3,1,4,1,6,1 = 47.32; 4,2,1,3,1,6,1 = 46.58; 4,2,1,4,1,6,1 = 46.31.
Final: p3. Confidence medium (F1 0.51, rule is clean board pattern, low band diffuse).
