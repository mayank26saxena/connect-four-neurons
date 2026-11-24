# histogram: estimated population share firing vs not, per (outcome, nfull) cell, col1-full positions only
import re,sys
sys.path.insert(0,'.')
from collections import Counter, defaultdict
from c4n.ns import board_from_moves
g={}; exec(compile(open('ns/work/U69/p3.py').read(),'p3','exec'),g)
W={0:.5/300,1:.3/300,2:.1/300,3:.05/300,4:.02/300,5:.01/300,6:.01/300,7:.005/300}
band=None; F=Counter(); N=Counter()
for fn in ['ns/work/U69/ex_low.txt','ns/work/U69/ex_hi.txt']:
  for l in open(fn).read().split('\n'):
    mb=re.match(r'=== band (\d)',l)
    if mb: band=int(mb.group(1))
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+).*moves: ([\d,]+)',l)
    if not m: continue
    b=board_from_moves([int(x) for x in m.group(3).split(',')])
    if b.heights[1]!=6: continue
    v=g['_outcome'](b)
    o='U' if v is None else ('L' if v<0 else ('D' if v==0 else 'W'))
    k=(o, sum(x==6 for x in b.heights))
    (F if band>=5 else N)[k]+=W[band]*1000
for k in sorted(set(F)|set(N)): print(k, "fire %.2f  not %.2f  (per mille of all positions)"%(F[k],N[k]))
