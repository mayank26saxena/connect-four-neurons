# histogram within col1-full & solver-lost: weighted fire vs not per feature value
import re,sys
sys.path.insert(0,'.')
from collections import Counter, defaultdict
from c4n.ns import board_from_moves
g={}; exec(compile(open('ns/work/U69/p3.py').read(),'p3','exec'),g)
W={0:.5/300,1:.3/300,2:.1/300,3:.05/300,4:.02/300,5:.01/300,6:.01/300,7:.005/300}
feats={
 'dist':lambda b,v:100+v,
 'mf_dist':lambda b,v:(b.me_first,100+v),
 'mf_nl':lambda b,v:(b.me_first,len(b.legal)),
 'me_first':lambda b,v:b.me_first,
 'nlegal':lambda b,v:len(b.legal),
 'last_col':lambda b,v:b.last_col,
 'lastrow':lambda b,v:b.last_row,
 'theirwins':lambda b,v:min(len(b.their_wins),4),
 'mywins':lambda b,v:min(len(b.my_wins),4),
 'mustblock':lambda b,v:len(b.their_playable_wins),
 'col1top':lambda b,v:b.grid[5][1],
 'col1row4':lambda b,v:b.grid[4][1],
 'col0':lambda b,v:b.heights[0],
 'col2':lambda b,v:b.heights[2],
 'col3':lambda b,v:b.heights[3],
 'col6':lambda b,v:b.heights[6],
 'empty':lambda b,v:42-b.ply,
}
F=defaultdict(Counter); N=defaultdict(Counter)
band=None
for fn in ['ns/work/U69/ex_low.txt','ns/work/U69/ex_hi.txt']:
  for l in open(fn).read().split('\n'):
    mb=re.match(r'=== band (\d)',l)
    if mb: band=int(mb.group(1))
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+).*moves: ([\d,]+)',l)
    if not m: continue
    b=board_from_moves([int(x) for x in m.group(3).split(',')])
    if b.heights[1]!=6: continue
    v=g['_outcome'](b)
    if v is None or v>=0: continue
    for n,f in feats.items():
        (F if band>=5 else N)[n][f(b,v)]+=W[band]*1000
for n in feats:
    ks=sorted(set(F[n])|set(N[n]),key=str)
    print(n,' '.join(f"{k}:{F[n][k]:.1f}/{N[n][k]:.1f}" for k in ks))
