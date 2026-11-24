import sys,re
sys.path.insert(0,'.')
from c4n.ns import board_from_moves
def load(files):
    bs=[]
    for f in files:
        for mv in re.findall(r"moves: ([\d,]+)",open(f).read()):
            bs.append(board_from_moves([int(x) for x in mv.split(',')]))
    return bs
lo=load(sys.argv[1].split(',')); hi=load(sys.argv[2].split(','))
for v,name in ((2,'O'),(1,'X'),(0,'empty')):
    print(name,'P(hi)-P(lo) per cell, top row first')
    for r in range(5,-1,-1):
        print(' '.join('%+.2f'%(sum(b.grid[r][c]==v for b in hi)/len(hi)-sum(b.grid[r][c]==v for b in lo)/len(lo)) for c in range(7)))
print('last col hi',[sum(b.last_col==c for b in hi) for c in range(7)],'lo',[sum(b.last_col==c for b in lo) for c in range(7)])
print('last row hi',[sum(b.last_row==c for b in hi) for c in range(6)],'lo',[sum(b.last_row==c for b in lo) for c in range(6)])
print('mefirst hi',sum(b.me_first for b in hi)/len(hi),'lo',sum(b.me_first for b in lo)/len(lo))
