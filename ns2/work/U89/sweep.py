import subprocess, itertools
res=[]
for O in itertools.combinations(range(7),3):
    rest=[c for c in range(7) if c not in O]
    for X in itertools.combinations(rest,2):
        mv=[O[0],X[0],O[1],X[1],O[2]]
        s=",".join(map(str,mv))
        out=subprocess.run(["uv","run","python","scripts/31_ns_tool.py","act","U89","--moves",s],capture_output=True,text=True).stdout
        line=[l for l in out.splitlines() if "after  5" in l][0]
        a=float(line.split(":")[1].split()[0])
        row="".join("O" if c in O else "X" if c in X else "." for c in range(7))
        res.append((a,row))
res.sort(reverse=True)
for a,row in res[:40]: print("%.2f %s"%(a,row))
print("...")
for a,row in res[-10:]: print("%.2f %s"%(a,row))
