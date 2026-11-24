import random, subprocess, re, collections, sys
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 0)
N=int(sys.argv[2]) if len(sys.argv)>2 else 150
def win(g,r,c,p):
    for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
        n=1
        for s in (1,-1):
            rr,cc=r+s*dr,c+s*dc
            while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: n+=1; rr+=s*dr; cc+=s*dc
        if n>=4: return True
    return False
stat=collections.defaultdict(list)
for gi in range(N):
    g=[[0]*7 for _ in range(6)]; h=[0]*7; mv=[]; cells=[]
    while True:
        leg=[c for c in range(7) if h[c]<6]
        if not leg: break
        c=random.choice(leg); r=h[c]; p=len(mv)%2+1; g[r][c]=p; h[c]+=1; mv.append(c); cells.append((r,c))
        if win(g,r,c,p): mv.pop(); cells.pop(); break
    if len(mv)<2: continue
    out=subprocess.run(['uv','run','python','scripts/31_ns_tool.py','act','U02','--moves',','.join(map(str,mv))],capture_output=True,text=True).stdout
    acts=[float(x) for x in re.findall(r'after\s+\d+ moves \([\d,]+\): (-?[\d.]+)',out)]
    for i,a in enumerate(acts):
        r,c=cells[i]; stat[(r,c)].append(a)
print("mean act / fire rate by last cell (row r top=5)")
for r in range(5,-1,-1):
    print(r, ' '.join("%5.2f/%3.0f%%"%(sum(stat[(r,c)])/max(1,len(stat[(r,c)])), 100*sum(x>0.696 for x in stat[(r,c)])/max(1,len(stat[(r,c)]))) for c in range(7)))
