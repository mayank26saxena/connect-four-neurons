import subprocess, sys, re, os
def grab(band, n, seed):
    out = subprocess.run(["uv","run","python","scripts/31_ns_tool.py","examples","U89","--band",str(band),"--n",str(n),"--seed",str(seed)],capture_output=True,text=True).stdout
    blocks = out.split("[pos ")[1:]
    res=[]
    for bl in blocks:
        lines = bl.splitlines()
        rows = lines[1:7]
        res.append(rows)
    return res
for bands in [(0,1,2),(5,6),(7,8,9)]:
    cnt = {}
    tot=0
    for band in bands:
        for seed in (1,2):
            for rows in grab(band,40,seed):
                tot+=1
                for ri,row in enumerate(rows):
                    r=5-ri
                    for c,ch in enumerate(row):
                        cnt[(r,c,ch)]=cnt.get((r,c,ch),0)+1
    print("bands",bands,"n",tot)
    for r in range(3,-1,-1):
        print(" r%d  "%r + "  ".join("%2d/%2d"%(round(100*cnt.get((r,c,'X'),0)/tot),round(100*cnt.get((r,c,'O'),0)/tot)) for c in range(7)))
