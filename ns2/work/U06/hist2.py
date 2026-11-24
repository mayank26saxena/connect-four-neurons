import re,subprocess
def get(band,seed,n=60):
    out=subprocess.run(["uv","run","python","scripts/31_ns_tool.py","examples","U06","--band",str(band),"--n",str(n),"--seed",str(seed)],capture_output=True,text=True).stdout
    return [ [int(x) for x in m.split(",")] for m in re.findall(r"moves: ([0-9,]+)",out)]
for bands,label in [((0,1,2),"low"),((6,7,8,9),"high")]:
    G=[]
    for bd in bands:
        for s in (21,22): G+=get(bd,s)
    for par in (0,1):
        H=[g for g in G if len(g)%2==par]; n=len(H)
        if not n: continue
        F=[sum(g[0::2].count(c) for g in H)/n for c in range(7)]
        S=[sum(g[1::2].count(c) for g in H)/n for c in range(7)]
        last=[sum(g[-1]==c for g in H)/n for c in range(7)]
        print(label,"parity",par,"n",n)
        print("  first ",[round(x,2) for x in F])
        print("  second",[round(x,2) for x in S])
        print("  last  ",[round(x,2) for x in last])
