import sys,re,collections
def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            g=L[i+1:i+7][::-1]; a=float(re.search(r'pole act (\S+)',l).group(1)); lc=re.search(r'last move col (\S+)',l).group(1)
            mv=re.search(r'moves: ([\d,]*)',l).group(1)
            out.append((g,a,lc,mv))
    return out
P=parse(sys.argv[1])
H=lambda g,c: sum(g[r][c]!='.' for r in range(6))
print(collections.Counter((H(g,0),H(g,1)) for g,a,lc,mv in P).most_common(20))
# last move cell
c=collections.Counter()
for g,a,lc,mv in P:
    if lc!='None': col=int(lc); c[(H(g,col)-1,col)]+=1
print(c.most_common(20))
# who is to move
print(collections.Counter(len(mv.split(','))%2 for g,a,lc,mv in P))
