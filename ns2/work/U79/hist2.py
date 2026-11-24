import sys, re, collections
txt=sys.stdin.read()
blocks=re.findall(r"moves: ([0-9,]+)\s+last move col (\d)", txt)
D=[(0,1),(1,0),(1,1),(1,-1)]
def wins(g,p):
    s=set()
    for r in range(6):
        for c in range(7):
            for dr,dc in D:
                cells=[(r+k*dr,c+k*dc) for k in range(4)]
                if all(0<=a<6 and 0<=b<7 for a,b in cells):
                    v=[g[a][b] for a,b in cells]
                    if v.count(p)==3 and v.count(0)==1:
                        s.add(cells[v.index(0)])
    return s
C=collections.Counter(); T=collections.Counter(); B=collections.Counter(); n=0
for mv,lc in blocks:
    mv=[int(x) for x in mv.split(',')]
    g=[[0]*7 for _ in range(6)]; hh=[0]*7
    for i,c in enumerate(mv):
        g[hh[c]][c]=1+(i%2); hh[c]+=1
    p=1+((len(mv)-1)%2)
    c=mv[-1]; r=hh[c]-1
    g2=[row[:] for row in g]; g2[r][c]=0
    new=wins(g,p)-wins(g2,p)
    T[min(len(new),3)]+=1
    # horizontal neighbours same color
    nb=sum(1 for dc in(-1,1) if 0<=c+dc<7 and g[r][c+dc]==p)
    B[nb]+=1
print("newthreats",sorted(T.items()),"horizSameNbr",sorted(B.items()))
