import sys,re
# plain single-feature histograms by band from examples output
def boards(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            rows=L[i+1:i+7]; out.append((l,rows))
    return out
feat=sys.argv[1]
for bd in range(10):
    vals=[]
    for l,rows in boards(f'ns2/work/U88/ex_b{bd}.txt'):
        g=[[ {'.':0,'X':1,'O':2}[ch] for ch in rows[5-r]] for r in range(6)]
        h=[sum(1 for r in range(6) if g[r][c]) for c in range(7)]
        ply=sum(h)
        v=eval(feat)
        vals.append(v)
    from collections import Counter
    c=Counter(vals); print(bd, ' '.join(f'{k}:{c[k]}' for k in sorted(c)))
