# U10 notebook (layer 1, pole +, thr 0.195, dev max 1.704)

## Examples (band 9 x40, bands 0-8)
Top band almost always: column 2 empty (or 1 stone) while columns 1 and 3 (and often 0) are tall -> a deep "well" at col 2.
Lower firing bands: other wells (e.g. col 5 between tall 4/6, col 3 between 2/4), plus some opening positions (first move in col 0 = 0.337).

## Hypotheses
H1: well depth at col 2: min(h1,h3) - h2 large.
H2: any column well (empty column between tall neighbours), col 2 weighted most.
H3: colour pattern of stones in col 1/3 modulates (act tests: same board heights, different colours: 0.129 vs 0.487).

## act tests
- single-column stacks: nothing fires except first move in col 0 (0.337).
- 1,1,3,3 x3 (cols 1,3 h=6, col2 empty): 0.487 fires; 1,3,3,1 x3 (same heights, other colours): 0.129.
- cols 0,1 full + col 3 full, col 2 empty: 0.707.
- adding 4 stones in col 4 to the 0.129 case: -0.094.
- 15442 trajectory: activation jumps as cols 1/3 grow with col 2 empty (0.15 -> 0.23 -> 0.31 -> 0.54 -> 1.36).

## Score calls
- call 1 (p1, output truncated, accidentally re-run) / call 2 p1 well depth min(h1,h3)-h2>=3: F1 0.115 (P 0.073 R 0.276), AUROC 0.585, sim share 0.11. Wells are far too common; most do not fire.
- call 3 p2 (well + last move in {0,1,3} + right-side penalty): F1 0.120 (P 0.159 R 0.097).
- More act tests: strong parity/colour dependence. Adding one far stone (flipping who is to move) often collapses activation (1.227 -> 0.001). Swapping the colours of the TOP stones in cols 1/3 barely matters (1.358 vs 1.513), but lower stones' colours do. Clean constructs: col0 all theirs + col1 all mine + col3 full + col2 empty = 1.76; reversed colours = 0.29-0.7. Contradicting probe: col1 theirs/col3 mine (1,3,1,3,1) = +0.20 vs reversed -0.36. No consistent per-column colour rule found.
- call 4 p3 (pure colour counts cols 0,1,3 minus col-2 height): F1 0.098. Colour counts alone fail (e.g. 13509 col3 short -> -1.2).
- call 5 p4 (opening move 0 at ply 1 OR col2 <=1 stone with col3>=4, col1>=2, left heavy and right light): F1 0.250 (P 0.305 R 0.212), AUROC 0.599, sim share 0.11.
- call 6 p5 = p4 + colour terms (my stones in col3, their stones in col0): F1 0.254. Negligible gain; keep simpler p4.
- Firing near threshold also includes other wells (col 3 empty between full cols 2/4, col 5 wells) in late games, and the opening position after a first move in column 0 (always 0.337).

## Steer
3+ positions (15442, 14394, 118338, the 1,1,3,3 construct, 0,5,0): forcing to zero or to max changes move probabilities by <= 0.01. No measurable effect.

## Synthesis
0,0,5,3,3,0,3,0,0,4,4,3,3,6,5,1,1,0,1,3 = 1.869 (beats dev max 1.704). Others 1.66, 1.63, 1.58, 0.98 (clean construct).

## Conclusion
Low confidence: best F1 0.25. The unit prefers a left-heavy board with column 2 (nearly) empty between tall columns 1 and 3 (col 0 also filled, right side short), but is strongly modulated by stone colours / side to move in a way I could not pin down; looks like a mixture.
