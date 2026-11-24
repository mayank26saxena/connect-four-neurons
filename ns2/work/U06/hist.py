import sys,re,subprocess
def get(band,seed,n=60):
    out=subprocess.run(["uv","run","python","scripts/31_ns_tool.py","examples","U06","--band",str(band),"--n",str(n),"--seed",str(seed)],capture_output=True,text=True).stdout
    return [ [int(x) for x in m.split(",")] for m in re.findall(r"moves: ([0-9,]+)",out)]
for bands,label in [((0,1),"low"),((3,4),"near"),((6,7,8,9),"high")]:
    G=[]
    for bd in bands:
        for s in (11,12): G+=get(bd,s)
    n=len(G)
    h=[sum(g.count(c) for g in G)/n for c in range(7)]
    odd=sum(len(g)%2 for g in G)/n
    ply=sum(len(g) for g in G)/n
    last=[sum(g[-1]==c for g in G)/n for c in range(7)]
    # stones by last mover (opponent) vs me per column
    opp=[sum(g[len(g)-1::-2].count(c) for g in G)/n for c in range(7)]
    print(label,n,"ply%.1f odd%.2f"%(ply,odd))
    print(" heights",[round(x,2) for x in h])
    print(" opp    ",[round(x,2) for x in opp])
    print(" last   ",[round(x,2) for x in last])
