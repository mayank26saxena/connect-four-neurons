import re
from collections import Counter
def lines():
    L=[]
    for r in range(6):
        for c in range(7):
            for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
                cells=[(r+dr*k,c+dc*k) for k in range(4)]
                if all(0<=a<6 and 0<=b<7 for a,b in cells): L.append(cells)
    return L
LN=lines()
D={}
for line in open('ex.txt'):
    b=line.split()[0]; m=re.search(r'moves: ([0-9,]+)',line).group(1)
    mv=[int(x) for x in m.split(',')]
    h=[0]*7; g=[[0]*7 for _ in range(6)]
    for i,c in enumerate(mv):
        g[h[c]][c]=1+(i%2); h[c]+=1
    me=1+(len(mv)%2)
    G=[[0 if v==0 else (1 if v==me else 2) for v in r] for r in g]
    tw=set(); mw=set()
    for L in LN:
        v=[G[a][b] for a,b in L]
        for p,s in ((2,tw),(1,mw)):
            if v.count(p)==3 and v.count(0)==1: s.add(L[v.index(0)])
    k=('lo' if b in('B0','B1') else 'hi')+('E' if len(mv)<12 else 'L')
    D.setdefault(k,[]).append((tw,mw))
for k,v in sorted(D.items()):
    n=len(v)
    print(k,n,'their threats rows',dict(sorted(Counter(r for tw,mw in v for r,c in tw).items())),'cols',dict(sorted(Counter(c for tw,mw in v for r,c in tw).items())))
    print('      my threats rows',dict(sorted(Counter(r for tw,mw in v for r,c in mw).items())),'cols',dict(sorted(Counter(c for tw,mw in v for r,c in mw).items())))
