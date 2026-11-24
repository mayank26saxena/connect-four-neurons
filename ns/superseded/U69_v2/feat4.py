import re,sys
sys.path.insert(0,'.')
from collections import Counter, defaultdict
from c4n.ns import board_from_moves
g={}; exec(compile(open('ns/work/U69/p3.py').read(),'p3','exec'),g)
band=None; d=defaultdict(Counter)
for fn in ['ns/work/U69/ex_low.txt','ns/work/U69/ex_hi.txt']:
  for l in open(fn).read().split('\n'):
    mb=re.match(r'=== band (\d)',l)
    if mb: band=int(mb.group(1))
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+).*moves: ([\d,]+)',l)
    if not m: continue
    b=board_from_moves([int(x) for x in m.group(3).split(',')])
    c1=b.heights[1]==6
    v=g['_outcome'](b) if c1 else 'x'
    lost = v not in ('x',None) and v<0
    nl=len(b.legal)
    d[band][(c1, lost, min(nl,4))]+=1
for k in sorted(d): print(k, sorted(d[k].items(),key=str))
