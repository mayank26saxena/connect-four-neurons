import re
from c4n.ns import board_from_moves
rows=[]
for fn in ['ns/work/U67/ex300.txt','ns/work/U67/ex300b.txt']:
  for line in open(fn):
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+).*moves: ([\d,]*)',line)
    if m:
        mv=[int(x) for x in m.group(3).split(',') if x]
        b=board_from_moves(mv)
        if b.heights[1]==0 and b.ply>=6: rows.append((float(m.group(2)),b))
for lo,hi in [(-99,1.146),(3,99)]:
    s=[b for a,b in rows if lo<=a<hi]
    print(lo,hi,len(s))
    for v,name in [(2,'O'),(1,'X')]:
        print(' ',name)
        for r in range(5,-1,-1):
            print('   ',' '.join('%3d'%round(100*sum(b.grid[r][c]==v for b in s)/len(s)) for c in range(7)))
    print('  me_first frac', sum(b.me_first for b in s)/len(s))
