import re
from c4n.ns import board_from_moves
rows=[]
for fn in ['ns/work/U67/ex300.txt','ns/work/U67/ex300b.txt']:
  for line in open(fn):
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+).*moves: ([\d,]*)',line)
    if m:
        mv=[int(x) for x in m.group(3).split(',') if x]
        rows.append((float(m.group(2)),board_from_moves(mv)))
for lo,hi in [(0,10),(10,20),(20,30),(30,42)]:
    for alo,ahi,name in [(-99,1.146,'nofire'),(1.146,99,'fire')]:
        s=[b for a,b in rows if alo<=a<ahi and lo<=b.ply<hi]
        if s: print(lo,hi,name,len(s),'me_first %.2f'%(sum(b.me_first for b in s)/len(s)), 'h1=0 %.2f'%(sum(b.heights[1]==0 for b in s)/len(s)), 'O in c1/c2 bottom %.2f'%(sum(b.grid[0][1]==2 or b.grid[0][2]==2 for b in s)/len(s)))
