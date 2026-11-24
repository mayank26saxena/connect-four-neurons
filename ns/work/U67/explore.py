import re,sys
from c4n.ns import board_from_moves
rows=[]
for line in open('ns/work/U67/ex300.txt'):
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+).*moves: ([\d,]*)',line)
    if m:
        mv=[int(x) for x in m.group(3).split(',') if x]
        rows.append((float(m.group(2)),board_from_moves(mv)))
def feats(b):
    g=b.grid
    f={}
    for c in range(7):
        f['O_c%d'%c]=sum(g[r][c]==2 for r in range(6))
        f['X_c%d'%c]=sum(g[r][c]==1 for r in range(6))
    f['h1']=b.heights[1]; f['h2']=b.heights[2]
    f['bot']=''.join('.XO'[g[0][c]] for c in range(7))
    return f
for lo,hi in [(-99,0.5),(0.5,1.146),(1.146,3),(3,99)]:
    s=[feats(b) for a,b in rows if lo<=a<hi]
    print(lo,hi,len(s))
    for k in ['O_c%d'%c for c in range(7)]+['X_c%d'%c for c in range(7)]:
        print('  %s mean %.2f  zero %.2f'%(k,sum(x[k] for x in s)/len(s),sum(x[k]==0 for x in s)/len(s)))
