import json, sys
prog = open(sys.argv[1]).read()
d = {
 "unit": "U12",
 "description": "Fires when the side to move has a game-winning, practically unstoppable position, mostly an immediate winning drop: strongest (top band) when the winning landing cell has another of my winning cells directly above it (typically centre column 3, row 1, in a late, crowded board), also on two simultaneous immediate wins and on lone immediate wins after move 14. Early single wins, vertical wins and losing double must-blocks are weak.",
 "effect": "Small: in decided positions it keeps probability on the winning column (zeroing it removes about 7-8 points from the winning move and spreads them to other columns; forcing it high adds about 1-2 points).",
 "program": prog,
 "synthesis": [
  [0,2,2,0,0,5,2,4,3,5,4,4,1,0,1,0,6,5,1,1,6,1,6,6,4,2],
  [0,2,2,0,0,5,2,4,3,5,4,4,1,0,1,0,6,5,1,1,6,1,6,6,6,4],
  [0,2,2,0,0,5,2,4,3,5,4,4,1,0,1,0,6,5,1,1,6,1,6,6,4,2,6,6],
  [0,2,2,0,0,5,2,4,3,5,4,4,1,0,1,0,6,5,1,1,6,1,6,6,6,2],
  [0,2,2,0,0,5,2,4,3,5,4,4,1,0,1,0,6,5,1,1,6,1,6,6]
 ],
 "confidence": "medium",
 "notes": "Best dev F1 0.671 (P 0.58, R 0.80, AUROC 0.89), sim share 1.64. Unit tracks 'won regardless of my move' (teacher scores ~+970 for most legal moves); immediate wins are the common board-visible case. Misses: forced wins with no immediate win (3+ threat cells, stacked threats above the landing cell) but adding those rules as board patterns gave many false positives (F1 0.28, 0.39). Single wins that are also the opponent's must-block still often fire. FPs mostly sit just under threshold (act 4.0-4.4)."
}
json.dump(d, open(sys.argv[2], "w"), indent=1)
