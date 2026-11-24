# U03 notebook (layer 3, pole +, thr 0.791, dev max 9.223)

## Observations (examples, ~80 viewed across bands)
- Nearly every firing example in bands 8-9 has column 5 holding exactly one stone (landing cell (1,5) empty).
- Early-game top: opponent stones on bottom row at cols 3 and 5 (e.g. 2,4,5,6,3 -> 3.37), plus O at (1,4) boosts (4,5,6,4,0,3 -> 7.0).
- Late-game top: O on row1 at cols 3,4 with (1,5) empty landing.

## Hypotheses
H1: fires when (1,5) is the landing cell of col 5 and opponent stones sit around it (0,3),(0,5),(1,3),(1,4).
H2: opponent horizontal/V pattern feeding the cell (1,5) (opponent-threat geometry) -- partly contradicted: O(0,3) is not on a line through (1,5) but matters.
H3: generic translation-invariant opponent "split pair" on bottom row -- REJECTED: shifting 4,5,6,3 left by 1-3 cols kills it (0.0-0.2), mirror kills it.

## Minimal pairs (act)
- 4,5,6,3 = 3.54 ; 4,5,6,2 = 0.56 ; 4,5,6,0 = 0.57 ; 0,5,6,3 (no X at (0,4)) = 1.89 ; 5,3,6,4 (colours swapped at 3/5 region) = 0.21
- Fill (1,5) by either side: 4,5,6,4,0,3 = 7.0 -> +5/0 -> 1.4. (1,5) empty is necessary-ish.
- (1,5) X/O : 4,5,6,3,0,5 1.36 ; 4,5,6,3,5,0 1.36 vs 4,5,6,3,0,4 6.06
- move order matters: 4,4,6,5 = 0.39 vs 4,5,6,4 = 0.97 (same board); 0,3,6,5 0.94 vs 0,5,6,3 1.89.
- 4,5,3,4,3,3 = -0.28 (X at (1,3)) vs 4,5,6,4,3,3 = 3.5
- Not mirror symmetric: mirror of 4,5,6,4,0,3,1,1 (9.58) gives -0.10.

## score 1 (p1: h5==1 & >=2 opp stones among (0,3),(1,4),(1,3),(0,5)): F1 0.241 P 0.154 R 0.557, AUROC 0.73, sim share 0.05
## score 2 (p2: weighted cell sum, h5==1 required): F1 0.291 P 0.259 R 0.334, sim share 0.13
- Single-cell histograms by band (420 examples): (1,5) empty in 95-100% of bands 6-9 vs ~35% in band 1; (0,5) O 70-80% vs 48%;
  (0,6) X 66-83% vs 41%; (0,4) never empty in top bands; (1,3) X 6% top vs 38% low; (1,4) O 58% vs 33%. Early game (ply<10) over-represented in top bands.
- Minimal pairs on 4,5,6,4,0,3 (7.0): X at (1,3) -> 1.7 (strong inhibitor); other single additions 2.8-6.9.
- steer: effect tiny (<=0.10 prob on any column) in 4 positions.
## score 3 (p3: p2 + (1,3)X penalty, (0,4)/(0,3) empty penalty, early-ply bonus, thr 5): F1 0.292 P 0.368 R 0.242, sim share 0.20
- Misses include late positions with (0,4)=O, (0,6)=O but O at (1,3),(1,4) next to empty (1,5). Over-weighted (0,6)/(0,4) colour.
- facts on 4 firing positions: no common threat concept (sometimes (1,5) is a must-block, often no threats at all).
## score 4 (p4: p3 with (0,6)/(0,4) colour weights cut, thr 4): F1 0.261 P 0.315 R 0.223 -- worse; colour of (0,6) does help precision.
- More act: activation depends on move ORDER for identical boards (4,3,6,0 0.49 vs 4,0,6,3 0.83; 4,4,6,5 0.39 vs 4,5,6,4 0.97), so a pure board rule has a ceiling.
- Some firing with col5 empty: ..OOX.X (0.94), O..OX.X (0.83).
## score 5 (p5: h5==1, h3,h4>=1, (1,3)!=X, opp at (0,5) or (1,4); count opp in {(0,3),(0,5),(1,3),(1,4)} + (0,6)X + early >=3): F1 0.311 P 0.279 R 0.352, sim 0.11
- FPs: (0,5)=X with lone O at (1,4); fix: require (0,5)=O, or O at both (1,3),(1,4).
## score 6 (p6: p5 but (0,5)=O or both (1,3),(1,4)=O): F1 0.310 P 0.282 R 0.344, sim 0.10 -- plateau at ~0.31. Stopped scoring (2 calls unused).
## steer (5 positions: 4,5,6,3; 42884; 8805; 97721; 4,5,6,4,1,1,0,3): changes <= 0.10 in any column; mostly <0.03. Effect ~none.
## synthesis: 4,5,6,4,1,1,0,3 = 10.72 (beats 9.22); 4,5,6,4,0,3,1,1 = 9.58 (beats); 4,5,6,4,0,1,1,3 = 7.93; 4,5,6,4,1,1,0,2,0,3 = 7.13; 4,5,6,4,0,3 = 7.01
## Conclusion: low confidence. Unit is anchored to column 5 holding one stone (landing (1,5) empty) with opponent stones around cols 3-5 on the bottom two rows,
   but is also sensitive to move order and to many other cells; best board rule F1 0.31. Final program = p5.
