import glob,re
acc={"them":[[] for _ in range(7)],"me":[[] for _ in range(7)],"last":[[] for _ in range(7)]}
for f in sorted(glob.glob("pr_*.txt"))+["probe_162049.txt","probe_37478.txt"]:
    L=open(f).read().splitlines()
    rows=[l for l in L[1:] if "who=" in l]
    n=len(rows)
    for k,l in enumerate(rows):
        p=l.split()
        who=p[1].split("=")[1]; vals=p[3:]
        v=[None if x=="." else float(x) for x in vals]
        ok=[x for x in v if x is not None]
        if len(ok)<3: continue
        mu=sum(ok)/len(ok)
        key="last" if k==n-1 else who
        for c in range(7):
            if v[c] is not None: acc[key][c].append((v[c]-mu)*1000)
for k in acc:
    print(k.ljust(5)," ".join("%+.2f(%d)"%(sum(a)/len(a),len(a)) if a else "  na  " for a in acc[k]))
