import subprocess
def grab(band, n, seed):
    out = subprocess.run(["uv","run","python","scripts/31_ns_tool.py","examples","U89","--band",str(band),"--n",str(n),"--seed",str(seed)],capture_output=True,text=True).stdout
    res=[]
    for bl in out.split("[pos ")[1:]:
        lines=bl.splitlines()
        mv=lines[0].split("moves: ")[1].split()[0]
        res.append((len(mv.split(",")), lines[1:7]))
    return res
for band in range(10):
    ps=[]; h1=[]; h3=[]
    for seed in (1,2):
        for ply,rows in grab(band,40,seed):
            ps.append(ply)
            h1.append(sum(1 for r in rows if r[1]!='.'))
            h3.append(sum(1 for r in rows if r[3]!='.'))
    ps.sort()
    bins=[0]*5
    for p in ps: bins[min(4,(p-4)//8)]+=1
    print(band, "ply bins 4-11,12-19,20-27,28-35,36+:",bins, " mean h1 %.1f h3 %.1f"%(sum(h1)/len(h1),sum(h3)/len(h3)))
