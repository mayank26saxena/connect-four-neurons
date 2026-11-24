import sys,re
from collections import defaultdict
from c4n.ns import board_from_moves
band=None; recs=defaultdict(list)
for line in open(sys.argv[1]):
    m=re.match(r'=== band (\d)',line)
    if m: band=int(m.group(1)); continue
    m=re.search(r'moves: ([\d,]+)\s+last move col',line)
    if m and band is not None:
        mv=[int(x) for x in m.group(1).split(",")]
        if int(sys.argv[2])<=len(mv)<=int(sys.argv[3]): recs[band>=5].append(board_from_moves(mv))
def show(name,fn):
    print('==',name,' (fire% - nonfire%)')
    for r in range(5,-1,-1):
        row=[]
        for c in range(7):
            p=[sum(fn(b,r,c) for b in recs[k])/len(recs[k]) for k in (True,False)]
            row.append('%+4d'%round(100*(p[0]-p[1])))
        print(' '.join(row))
show('mine',lambda b,r,c:b.grid[r][c]==1)
show('theirs',lambda b,r,c:b.grid[r][c]==2)
show('empty',lambda b,r,c:b.grid[r][c]==0)
show('theirwin',lambda b,r,c:(r,c) in b.their_wins)
show('mywin',lambda b,r,c:(r,c) in b.my_wins)
show('last',lambda b,r,c:(b.last_row,b.last_col)==(r,c))
