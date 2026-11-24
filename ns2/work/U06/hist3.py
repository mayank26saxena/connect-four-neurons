import re,subprocess
def get(band,seed,n=60):
    out=subprocess.run(["uv","run","python","scripts/31_ns_tool.py","examples","U06","--band",str(band),"--n",str(n),"--seed",str(seed)],capture_output=True,text=True).stdout
    return [ [int(x) for x in m.split(",")] for m in re.findall(r"moves: ([0-9,]+)",out)]
for bands,label in [((0,1,2,3),"low"),((6,7,8,9),"high")]:
    G=[]
    for bd in bands:
        for s in (31,32,33): G+=get(bd,s)
    for lc in (1,2,3):
        H=[g for g in G if g[-1]==lc]; n=len(H)
        if not n: continue
        T=[sum(g[len(g)-1::-2].count(c) for g in H)/n for c in range(7)]
        M=[sum(g[len(g)-2::-2].count(c) for g in H)/n for c in range(7)]
        ply=sum(len(g) for g in H)/n
        print(label,"last",lc,"n",n,"ply %.1f"%ply)
        print("  them",[round(x,2) for x in T])
        print("  me  ",[round(x,2) for x in M])
