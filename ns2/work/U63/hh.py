import sys
from collections import Counter
from c4n.ns import board_from_moves
c=int(sys.argv[1]); cnt=Counter(); n=0
for line in sys.stdin:
    if not line.startswith('[pos'): continue
    mv=[int(x) for x in line.split('moves: ')[1].split()[0].split(',')]
    b=board_from_moves(mv); cnt[b.heights[c]]+=1
print(dict(sorted(cnt.items())))
