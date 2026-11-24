import sys
from c4n.ns import board_from_moves
grids={1:[[0]*7 for _ in range(6)],2:[[0]*7 for _ in range(6)]}; n=0
for line in sys.stdin:
    if not line.startswith('[pos'): continue
    mv=[int(x) for x in line.split('moves: ')[1].split()[0].split(',')]
    b=board_from_moves(mv); n+=1
    for r in range(6):
        for c in range(7):
            v=b.grid[r][c]
            if v: grids[v][r][c]+=1
for v,name in ((1,'mine'),(2,'theirs')):
    print(name, 'n=',n)
    for r in range(3,-1,-1):
        print(' '.join('%3d'%(100*grids[v][r][c]//n) for c in range(7)))
