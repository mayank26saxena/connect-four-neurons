# exploration: compare simple features of col1-full & solver-lost positions, firing vs not
import re,sys
sys.path.insert(0,'.')
from collections import Counter
from c4n.ns import board_from_moves
g={}; exec(compile(open('ns/work/U69/p3.py').read(),'p3','exec'),g)
def load(fn):
    out=[]
    for l in open(fn).read().split('\n'):
        m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+).*moves: ([\d,]+)',l)
        if not m: continue
        a=float(m.group(2)); b=board_from_moves([int(x) for x in m.group(3).split(',')])
        if b.heights[1]!=6: continue
        v=g['_outcome'](b)
        out.append((a,b,v))
    return out
lo=load('ns/work/U69/ex_low.txt'); hi=load('ns/work/U69/ex_hi.txt')
print("low col1full",len(lo),"outcomes",Counter(v for a,b,v in lo if True and (v is None or True)).most_common(6) if False else Counter((None if v is None else (v>0)-(v<0)) for a,b,v in lo))
print("hi col1full",len(hi),Counter((None if v is None else (v>0)-(v<0)) for a,b,v in hi))
L=[(a,b) for a,b,v in lo if v is not None and v<0]; H=[(a,b) for a,b,v in hi if v is not None and v<0]
feats={
 'empty':lambda b:42-b.ply,
 'me_first':lambda b:b.me_first,
 'nlegal':lambda b:len(b.legal),
 'col3open':lambda b:b.heights[3]<6,
 'last_col':lambda b:b.last_col,
 'theirwins':lambda b:min(len(b.their_wins),4),
 'mywins':lambda b:min(len(b.my_wins),4),
 'mustblock':lambda b:len(b.their_playable_wins),
 'col1top_mine':lambda b:b.grid[5][1],
 'col0full':lambda b:b.heights[0]==6,
 'col2full':lambda b:b.heights[2]==6,
}
for n,f in feats.items():
    cl=Counter(f(b) for a,b in L); ch=Counter(f(b) for a,b in H)
    ks=sorted(set(cl)|set(ch),key=str)
    print(n, ' '.join(f"{k}:{cl[k]}/{ch[k]}" for k in ks))
