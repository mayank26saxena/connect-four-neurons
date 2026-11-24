import itertools,subprocess,sys
base=[2,3,2,3,2,3,2,3]
seen=set();res=[]
for p in set(itertools.permutations(base)):
    n=len(p);g={2:'',3:''}
    for i,c in enumerate(p): g[c]+= 'X' if i%2==n%2 else 'O'
    key=(g[2],g[3])
    if key in seen: continue
    seen.add(key)
    s=','.join(map(str,p))
    out=subprocess.run(['uv','run','python','scripts/31_ns_tool.py','act','U39','--moves',s],capture_output=True,text=True).stdout
    v=[l for l in out.splitlines() if 'after  8' in l][0].split(':')[-1].split()[0]
    res.append((float(v),g[2],g[3],s))
for r in sorted(res,reverse=True): print(r)
