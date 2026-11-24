# hill-climb synthesis: mutate move order among same-player moves, keep col-1 third stone last
import subprocess, random, re, sys
random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 0)
def act(mv):
    out = subprocess.run(["uv","run","python","scripts/31_ns_tool.py","act","U47","--moves",",".join(map(str,mv))],capture_output=True,text=True).stdout
    vals = re.findall(r"after\s+\d+ moves \([^)]*\): (-?[\d.]+)", out)
    if not vals or len(vals) < len(mv): return None
    return float(vals[-1])
def legal(mv):
    h=[0]*7
    for x in mv:
        h[x]+=1
        if h[x]>6: return False
    return h[1]==3
best=[int(x) for x in sys.argv[1].split(',')]
bv=act(best); print('start',bv,flush=True)
for it in range(int(sys.argv[3]) if len(sys.argv)>3 else 40):
    cand=best[:]
    k=random.choice([0,1,2])
    if k==0:
        i,j=random.sample(range(len(cand)-1),2)
        if (i-j)%2: continue
        cand[i],cand[j]=cand[j],cand[i]
    elif k==1:
        i=random.randrange(len(cand)-1); cand[i]=random.randrange(7)
    else:
        i=random.randrange(len(cand)-1)
        cand=cand[:i]+[random.randrange(7),random.randrange(7)]+cand[i:]
    if not legal(cand): continue
    v=act(cand)
    if v is not None and v>bv:
        best,bv=cand,v; print(it,bv,','.join(map(str,best)),flush=True)
print('final',bv,','.join(map(str,best)))
