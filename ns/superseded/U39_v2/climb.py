import subprocess,random
random.seed(0)
def act(seq):
    h=[0]*7
    for c in seq:
        if h[c]>=6: return None
        h[c]+=1
    out=subprocess.run(['uv','run','python','scripts/31_ns_tool.py','act','U39','--moves',','.join(map(str,seq))],capture_output=True,text=True).stdout
    l=[x for x in out.splitlines() if 'after' in x][-1]
    return float(l.split('):')[1].split()[0])
best=[2,3,2,3,3,2,2,3,5,0,1,0];bv=act(best)
for it in range(90):
    s=best[:]
    r=random.random()
    if r<0.7: s[random.randrange(len(s))]=random.randrange(7)
    elif r<0.85: s=s+[random.randrange(7),random.randrange(7)]
    elif len(s)>8: s=s[:-2]
    v=act(s)
    if v is not None and v>bv:
        best,bv=s,v;print(it,bv,best,flush=True)
print('final',bv,best)
