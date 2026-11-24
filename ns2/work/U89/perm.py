import subprocess, itertools
A=[3,4,0,4]; B=[5,2,2,5]
seen=set(); res=[]
for pa in set(itertools.permutations(A)):
    for pb in set(itertools.permutations(B)):
        mv=[]
        for i in range(4): mv+= [pa[i],pb[i]]
        mv.append(2)
        s=",".join(map(str,mv))
        out=subprocess.run(["uv","run","python","scripts/31_ns_tool.py","act","U89","--moves",s],capture_output=True,text=True).stdout
        l=[x for x in out.splitlines() if "after  9" in x][0]
        res.append((float(l.split(":")[1].split()[0]),s))
res.sort(reverse=True)
for r in res[:5]: print(r)
