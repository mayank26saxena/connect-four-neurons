# hill-climb synthesis sequences using the act tool
import random, subprocess, sys, re
def wins(g, r, c, p):
    for dr, dc in ((0,1),(1,0),(1,1),(1,-1)):
        n = 1
        for s in (1,-1):
            rr, cc = r+dr*s, c+dc*s
            while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p:
                n += 1; rr += dr*s; cc += dc*s
        if n >= 4: return True
    return False
def valid(seq):
    g=[[0]*7 for _ in range(6)]; h=[0]*7
    for i,c in enumerate(seq):
        if h[c]>=6: return False
        p=1+i%2; g[h[c]][c]=p; h[c]+=1
        if wins(g,h[c]-1,c,p): return False
    return True
def act(seq):
    out=subprocess.run(["uv","run","python","scripts/31_ns_tool.py","act","U42","--moves",",".join(map(str,seq))],capture_output=True,text=True).stdout
    m=re.findall(r"after +\d+ moves \([^)]*\): (-?[\d.]+)",out)
    return float(m[-1])
best=[int(x) for x in sys.argv[1].split(",")]
bv=act(best); print(bv, flush=True)
random.seed(int(sys.argv[2]))
for it in range(int(sys.argv[3])):
    s=best[:]
    k=random.choice([0,1,2])
    if k==0:
        i=random.randrange(len(s)-1); s[i]=random.randrange(7)
    elif k==1 and len(s)>8:
        i=random.randrange(len(s)-3); del s[i:i+2]
    else:
        i=random.randrange(len(s)-1); s[i:i]=[random.randrange(7),random.randrange(7)]
    if s[-1]!=0 or not valid(s): continue
    v=act(s)
    if v>bv:
        bv,best=v,s; print(bv, ",".join(map(str,best)), flush=True)
print("BEST",bv,",".join(map(str,best)))
