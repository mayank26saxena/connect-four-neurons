import sys
from collections import Counter
from c4n.ns import board_from_moves
cnt=Counter();n=0
for line in sys.stdin:
    if not line.startswith('[pos'): continue
    mv=[int(x) for x in line.split('moves: ')[1].split()[0].split(',')]
    b=board_from_moves(mv)
    if not (11<=b.ply<=22): continue
    n+=1; cnt[sum(h==0 for h in b.heights)]+=1
print(n, dict(sorted(cnt.items())))
