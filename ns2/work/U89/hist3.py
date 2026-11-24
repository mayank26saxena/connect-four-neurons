import subprocess
def grab(band, n, seed):
    out = subprocess.run(["uv","run","python","scripts/31_ns_tool.py","examples","U89","--band",str(band),"--n",str(n),"--seed",str(seed)],capture_output=True,text=True).stdout
    res=[]
    for bl in out.split("[pos ")[1:]:
        lines=bl.splitlines()
        mv=[int(x) for x in lines[0].split("moves: ")[1].split()[0].split(",")]
        res.append(mv)
    return res
for bands in [(0,1),(2,3,4),(5,6),(7,8,9)]:
    lc=[0]*7; H=[0]*7; n=0; par=0
    for band in bands:
        for seed in (1,2,3):
            for mv in grab(band,40,seed):
                if len(mv)>16: continue
                n+=1; lc[mv[-1]]+=1; par+=len(mv)%2
                for c in range(7): H[c]+=mv.count(c)
    print(bands,"n",n,"(ply<=16) lastcol%",[round(100*x/n) for x in lc]," meanH",[round(h/n,1) for h in H]," odd-ply%",round(100*par/n))
