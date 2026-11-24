import subprocess, itertools, random
random.seed(0)
A=[4,4,0,3,0]; B=[2,2,5,5,0]
res=[]
def legal_order(pa,pb):
    mv=[]
    for i in range(5): mv+=[pa[i],pb[i]]
    mv.append(2)
    # col0 must be A,A,B order: check final stack equals target
    st={c:[] for c in range(7)}
    for i,m in enumerate(mv): st[m].append(i%2)
    return mv if st[0]==[0,0,1] and st[2]==[1,1,0] else None
cands=set()
for pa in set(itertools.permutations(A)):
    for pb in set(itertools.permutations(B)):
        mv=legal_order(pa,pb)
        if mv: cands.add(tuple(mv))
cands=random.sample(sorted(cands),min(150,len(cands)))
for mv in cands:
    s=",".join(map(str,mv))
    out=subprocess.run(["uv","run","python","scripts/31_ns_tool.py","act","U89","--moves",s],capture_output=True,text=True).stdout
    l=[x for x in out.splitlines() if "after 11" in x][0]
    res.append((float(l.split(":")[1].split()[0]),s))
res.sort(reverse=True)
for r in res[:5]: print(r)
