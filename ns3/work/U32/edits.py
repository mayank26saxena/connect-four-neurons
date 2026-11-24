# usage: edits.py BOARD mode ; BOARD rows top->bottom separated by '/'
# mode 'rm': remove one top X and one top O; 'add': add one X and one O on landing cells; prints seqs
import sys,itertools
sys.path.insert(0,'ns3/work/U32')
from build import build
rows=[r for r in sys.argv[1].split('/')]
while len(rows)<6: rows.insert(0,'.......')
g=[list(r) for r in rows[::-1]]  # g[r][c], r=0 bottom
def heights(g): return [sum(1 for r in range(6) if g[r][c]!='.') for c in range(7)]
def pic(g): return '/'.join(''.join(g[r]) for r in range(5,-1,-1))
out=[]
mode=sys.argv[2]
h=heights(g)
if mode=='rm':
    tops=[(h[c]-1,c) for c in range(7) if h[c]>0]
    for (rx,cx),(ro,co) in itertools.product(tops,tops):
        if g[rx][cx]!='X' or g[ro][co]!='O': continue
        if cx==co: continue
        g2=[row[:] for row in g]; g2[rx][cx]='.'; g2[ro][co]='.'
        out.append((f"-X{rx}{cx}-O{ro}{co}",g2))
    # also remove two stacked in same column (top two of different colors)
    for c in range(7):
        if h[c]>=2 and {g[h[c]-1][c],g[h[c]-2][c]}=={'X','O'}:
            g2=[row[:] for row in g]; g2[h[c]-1][c]='.'; g2[h[c]-2][c]='.'
            out.append((f"-col{c}x2",g2))
elif mode=='add':
    for cx in range(7):
        for co in range(7):
            g2=[row[:] for row in g]; hh=heights(g2)
            if hh[cx]>=6: continue
            g2[hh[cx]][cx]='X'; hh=heights(g2)
            if hh[co]>=6: continue
            g2[hh[co]][co]='O'
            out.append((f"+X{cx}+O{co}",g2))
elif mode=='flip':
    cells=[(r,c) for r in range(6) for c in range(7) if g[r][c]!='.']
    for (r1,c1),(r2,c2) in itertools.combinations(cells,2):
        if g[r1][c1]==g[r2][c2]: continue
        g2=[row[:] for row in g]; g2[r1][c1],g2[r2][c2]=g2[r2][c2],g2[r1][c1]
        out.append((f"sw{r1}{c1}-{r2}{c2}",g2))
for name,g2 in out:
    try:
        s=build(pic(g2).split('/'))
        print(name, ','.join(map(str,s)))
    except SystemExit as e:
        pass
