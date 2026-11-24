import random, subprocess, re
random.seed(1)
def act(mv):
    out=subprocess.run(['uv','run','python','scripts/31_ns_tool.py','act','U02','--moves',','.join(map(str,mv))],capture_output=True,text=True).stdout
    a=re.findall(r'after\s+\d+ moves \([\d,]+\): (-?[\d.]+)',out)
    return [float(x) for x in a]
best=[]
for seq in ([6,6,6],[0,6,6,6],[6,0,6,0,6]):
    acts=act(seq); best.append((acts[-1],seq))
for it in range(120):
    base=random.choice(sorted(best,reverse=True)[:5])[1]
    s=list(base)
    op=random.random()
    pos=random.randrange(len(s)+1)
    if op<0.5: s.insert(pos,random.randrange(7))
    elif op<0.8 and len(s)>1: s[random.randrange(len(s))]=random.randrange(7)
    elif len(s)>2: s.pop(random.randrange(len(s)))
    if max(s.count(c) for c in range(7))>6: continue
    acts=act(s)
    if len(acts)!=len(s): continue
    best.append((acts[-1],s))
for a,s in sorted(best,reverse=True)[:8]: print(a,s)
