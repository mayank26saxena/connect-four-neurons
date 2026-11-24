import sys,re,collections
def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            g=L[i+1:i+7][::-1]; a=float(re.search(r'pole act (\S+)',l).group(1)); out.append((g,a))
    return out
for fn in sys.argv[1:]:
    P=parse(fn)
    H=lambda g,c: sum(g[r][c]!='.' for r in range(6))
    print(fn)
    for c in range(7): print('col',c,sorted(collections.Counter(H(g,c) for g,a in P).items()))
    print('(0,1),(1,1),(2,1)', collections.Counter(g[0][1]+g[1][1]+g[2][1] for g,a in P).most_common(15))
