import sys
from c4n.ns import board_from_moves
feat = sys.argv[1]
from collections import Counter
cnt=Counter()
for line in sys.stdin:
    if not line.startswith('[pos'): continue
    mv=[int(x) for x in line.split('moves: ')[1].split()[0].split(',')]
    b=board_from_moves(mv)
    r,c=b.last_row,b.last_col
    if feat=='under':
        v = 'floor' if r==0 else ('mine' if b.grid[r-1][c]==1 else 'theirs')
    elif feat=='lastrow': v=r
    elif feat=='lastcol': v=c
    elif feat=='mefirst': v=b.me_first
    elif feat=='nmine_row0': v=sum(1 for cc in range(7) if b.grid[0][cc]==1)
    cnt[v]+=1
print(dict(sorted(cnt.items(),key=lambda x:str(x[0]))))
