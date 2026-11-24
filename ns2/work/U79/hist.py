import sys, re, collections
# reads examples output on stdin; histogram of vertical run length of last stone, and ply parity
txt=sys.stdin.read()
blocks=re.findall(r"moves: ([0-9,]+)\s+last move col (\d)", txt)
run=collections.Counter(); par=collections.Counter(); h=collections.Counter()
for mv,lc in blocks:
    mv=[int(x) for x in mv.split(',')]
    g=[[0]*7 for _ in range(6)]; hh=[0]*7
    for i,c in enumerate(mv):
        g[hh[c]][c]=1+(i%2); hh[c]+=1
    c=mv[-1]; r=hh[c]-1; p=g[r][c]; k=1
    while r-k>=0 and g[r-k][c]==p: k+=1
    run[k]+=1; par[len(mv)%2]+=1; h[r]+=1
print("run",sorted(run.items()),"parity",sorted(par.items()),"lastrow",sorted(h.items()))
