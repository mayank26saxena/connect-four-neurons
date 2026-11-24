import sys, re, collections
txt=sys.stdin.read()
blocks=re.findall(r"moves: ([0-9,]+)\s+last move col (\d)", txt)
C=collections.Counter()
for mv,lc in blocks:
    mv=[int(x) for x in mv.split(',')]
    g=[[0]*7 for _ in range(6)]; hh=[0]*7
    for i,c in enumerate(mv):
        g[hh[c]][c]=1+(i%2); hh[c]+=1
    p=1+((len(mv)-1)%2)
    c=mv[-1]
    s=''.join('O' if g[r][c]==p else 'x' for r in range(hh[c]))
    C[str(c)+':'+s]+=1
print(C.most_common(12))
