import sys,re
from c4n.ns import board_from_moves
rows=[]
for line in open(sys.argv[1]):
    m=re.search(r'\(([\d,]+)\): (-?[\d.]+)',line)
    if not m: continue
    mv=[int(x) for x in m.group(1).split(',')]; a=float(m.group(2))
    rows.append((mv,a,board_from_moves(mv)))
print(len(rows), 'fire', sum(a>0.679 for _,a,_ in rows))
# mean activation by (cell,owner)
for who,name in ((1,'mine'),(2,'theirs')):
    print(name,'mean act when cell occupied')
    for r in (1,0):
        out=[]
        for c in range(7):
            v=[a for _,a,b in rows if b.grid[r][c]==who]
            out.append('%5.2f'%(sum(v)/len(v)) if v else '  -  ')
        print(' '.join(out))
rows.sort(key=lambda x:-x[1])
for mv,a,b in rows[:25]: print(a, mv)
print('...')
for mv,a,b in rows[-10:]: print(a, mv)
