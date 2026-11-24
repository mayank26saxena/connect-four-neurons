# U32 notebook (layer 5, pole +, threshold 0.971, dev max 5.355)

## Observations
- Bands 7-9: column 1 has exactly one stone in ~94% (bottom cell filled, row 1 empty); bands 0-2: col1 height spread.
- Bands 5-6 (near threshold): many late-game boards with col1 full.
- Adding any stone to col1 (both colors) to firing positions kills activation (two-move grids from pos 112058 & 47355).
- Early positions: 2,4,0,4 (X at (0,0),(0,2), O at (0,4),(1,4)) = 4.0; X at (0,0) seems important in many 4-ply probes.
- steer: forcing unit off raises col1 prob a bit (+0.06/+0.08); forcing max lowers col1 by ~0.05. Small effect.
- No tactical threats in top examples (their/my threat cells empty).

## Hypotheses
H1: col1 height == 1 (landing cell (1,1)) with developed board elsewhere.
H2: some left-side diagonal pattern through (1,1) / me at (0,0). (minimal pairs inconsistent)
H3: random/distributed direction keyed on col1 height.

## Minimal-pair / edit sweeps (build.py + edits.py rebuild boards in any legal order; activation is mostly board-driven)
- 112058: removing O at (3,2) or flipping (3,3) to me kills; swapping (0,3)O<->(4,3)X gives 5.41 (beats dev max; them get vertical three in col 3).
- 166800: flipping (3,3) from them to me drops 3.5 -> -3.4. (3,3)=them matters there, but 57108 fires with (3,3) empty.
- 47355: every one-stone change lowers it; fragile, sequence-like.
- 4-stone probes: X at (0,0)+(0,2) with O stacked in col 4 = 4.0-4.3; X(0,1)+(0,2) = 0. No clean geometric rule.
- Adding any stone to col1 kills activation in every firing board tested.
- Ply histogram: high bands = ply 12-24; bands 2-5 = late-game boards (ply 30+) at modest activation.

## Scores
1. h1==1: F1 0.167 (P .098 R .565) AUROC .695, sim -0.07
2. h1==1 & h3>=4 & h0>=1 & h2>=1: F1 0.222 (P .17 R .32)
3. h1==1 & ((3,3)=them or col1 threat): F1 0.200
4. h1==1 & h0>=1 & 12<=ply<=26 & h2+h3>=7: F1 0.250 (P .225 R .281)  <- best
5. h1==1 & h0>=2 & h2>=2 & h3>=3: F1 0.190
6. p4 + h1==0 early: F1 0.136
Simulation share is negative for every program.

## Steer
Off: col1 +0.06/+0.08 when col1 is a live option; max: col1 -0.04/-0.05. Otherwise ~0. Small effect.

## Conclusion
Necessary-ish condition: column 1 holds exactly one stone (94% of top-band firing), in a mid-game board with the center built up.
Not sufficient: precision stays near 0.2. What else is needed looks like a configuration-specific mix (opponent stones around (3,2)/(3,3), me at (0,0)).
Confidence low.
