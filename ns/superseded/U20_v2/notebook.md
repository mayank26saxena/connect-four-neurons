# U20 lab notebook (layer 5, pole +, threshold 1.106, firing rate 1.7%, dev max 7.12)

## Observations (examples, ~270 firing positions from bands 7-9, 180 from bands 1-3)
- Empty board sits exactly at threshold (1.106) and does not fire.
- Firing positions: column 1 is NEVER empty, never full, almost never height 3. Heights 1 (28%), 2 (53%), 4-5 (18%).
  Column 0 is usually low (empty 49%, height 1 27%). Mostly early/middle game (ply 3-27).
- Last move often in col 1/2.
- Steering: forcing to 0 raises col 1 probability a little (+0.04..+0.16); forcing to max lowers col 1 (-0.02..-0.08).
  Small effect.

## Candidate hypotheses
H1: column-1 landing-cell feature: fires when col 1 has 1-2 stones (landing row 1-2) and col 0 lower than col 1.
H2: opponent threat to build an open three on a low row near the left side (from 3-ply sweep: O on (0,1),(0,2) with X far right fires; X at col 3/4 blocking does not).
H3: random/mixed direction with no clean rule.

## Tests
- 3-ply sweep (first move 1 or 2, then X a, O b): fires for O(0,1)+O(0,2) with X at col 5 (1.47-1.86), X at col 6 (1.08);
  not with X at col 0/3/4. Also O(0,1),O(1,2),X(0,2) = 2.0 (does not fit H2).
- 4,6,1,6,2,3 (3.85): changing any single key stone kills it (O's last 3->5: -0.21; X 1->0: 0.06; X 2->5: -0.05).
  Two-move continuation sweep is very noisy (values -1.25..3.05 without obvious pattern).

## Dev metric log
- call 1 (p1.py: h1 in {1,2,4,5}, h0<h1, ply<=28): F1 0.083 (P 0.044, R 0.677), AUROC 0.712, sim share -0.10.
- call 2 (p2.py: h1==2&h0<2 or h1==1&h0==0, no immediate win): F1 0.112 (P 0.062, R 0.535), AUROC 0.698, sim -0.08.
- call 3 (p3.py: p2 + col2>=1, col3>=2, exclude col1 = them-bottom/me-top): F1 0.164 (P 0.110, R 0.322), AUROC 0.639, sim -0.08. BEST.
- call 4 (p4.py: add h1==5, exclude must-blocks): F1 0.143 (P 0.087, R 0.388). Worse.

## Further tests (why I stopped)
- Threat-above-landing idea (threat cell at (h1+1,1), common in top examples): built a clean position with my threat at (3,1)
  above landing (2,1): 0.69, not firing. Rejected as sufficient cause.
- Teacher scores: col 1 is not consistently a bad move in firing positions.
- 1,2,2 fires (2.0) but adding almost ANY pair of stones elsewhere kills it (-0.7..1.0). 4,6,1,6,2,3 (3.85): every single-stone
  change tested drops it. Activation is fragile, configuration-specific and not monotone in any board concept I tried.
- Conclusion: the only robust regularity is column-1 / column-0 geometry (necessary-ish, far from sufficient). Looks like a
  mixture or random direction. Confidence low.

## Steering
Zeroing raises column 1 by +0.04..+0.16 in 6/7 positions; forcing max lowers col 1 by 0.01-0.08. Small.

## Synthesis
Base 3,4,6,1,3,6,3,3,3,1,6,2,4,4,6 (dev 5.91) + continuations: +6,0,4,4 = 8.95; +4,4,3,0 = 8.09; +4,4,6,0 = 8.03;
+4,4,2,0 = 7.82; +6,0 = 7.80. All beat the dev max 7.12.
