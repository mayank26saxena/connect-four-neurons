# histogram of last move col/row, ply parity, below-cell owner from examples text on stdin
import sys, re
txt=sys.stdin.read()
blocks=re.findall(r'\[pos (\d+)\] pole act ([-\d.]+).*?moves: ([\d,]*)\s+last move col (\w+).*?\n((?:[.XO]{7}\n){6})',txt)
seen=set(); lc={}; lr={}; par={}; below={}; ply=[]
for pid,a,mv,l,g in blocks:
    if pid in seen: continue
    seen.add(pid)
    rows=g.strip().split('\n'); grid=[[rows[5-r][c] for c in range(7)] for r in range(6)]
    if l=='None': continue
    c=int(l); h=sum(1 for r in range(6) if grid[r][c]!='.'); r=h-1
    lc[c]=lc.get(c,0)+1; lr[r]=lr.get(r,0)+1
    p=len(mv.split(',')); par[p%2]=par.get(p%2,0)+1; ply.append(p)
    bl = grid[r-1][c] if r>0 else 'floor'
    below[bl]=below.get(bl,0)+1
n=len(seen)
print('n',n,'lastcol',sorted(lc.items()),'lastrow',sorted(lr.items()),'parity',par,'below',below,'meanply',sum(ply)/max(1,len(ply)))
