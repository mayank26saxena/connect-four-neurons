import re
from c4n.ns import board_from_moves
rows=[]
for fn in ['ns/work/U67/ex300.txt','ns/work/U67/ex300b.txt']:
  for line in open(fn):
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+).*moves: ([\d,]*)',line)
    if m:
        mv=[int(x) for x in m.group(3).split(',') if x]
        rows.append((float(m.group(2)),board_from_moves(mv)))
s=[(a,b) for a,b in rows if a>1.146 and b.ply>=28]
for a,b in s[:14]:
    print(a, b.ply, b.me_first, 'heights',b.heights, 'mythreats',sorted(b.my_wins),'their',sorted(b.their_wins))
    print(b.render())
