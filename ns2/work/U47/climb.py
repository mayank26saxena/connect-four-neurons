import subprocess,random,re,sys,os
env=dict(os.environ)
def won(g,r,c,p):
    for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
        n=1
        for s in (1,-1):
            rr,cc=r+dr*s,c+dc*s
            while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: n+=1; rr+=dr*s; cc+=dc*s
        if n>=4: return True
    return False
def valid(m):
    g=[[0]*7 for _ in range(6)];h=[0]*7
    for i,c in enumerate(m):
        if h[c]>=6: return False
        p=1+i%2; g[h[c]][c]=p
        if won(g,h[c],c,p): return False
        h[c]+=1
    return len(m)>=4
def act(m):
    out=subprocess.run(['uv','run','python','scripts/31_ns_tool.py','act','U47','--moves',','.join(map(str,m))],capture_output=True,text=True,env=env).stdout
    v=re.findall(r"after +\d+ moves \([\d,]+\): ([-\d.]+)",out)
    return float(v[-1])
best=[int(x) for x in sys.argv[1].split(',')]; bv=act(best); print(bv,flush=True)
random.seed(int(sys.argv[2]))
for it in range(int(sys.argv[3])):
    m=list(best); k=random.random()
    if k<0.4:
        i=random.randrange(len(m)); m[i]=random.randrange(7)
    elif k<0.7:
        i,j=random.sample(range(len(m)),2)
        if (i-j)%2==0: m[i],m[j]=m[j],m[i]
        else: continue
    elif k<0.85:
        m=m+[random.randrange(7),random.randrange(7)]
    else:
        if len(m)<6: continue
        i=random.randrange(len(m)-1); i-=i%2 if random.random()<0.5 else 0
        del m[i:i+2]
    if not valid(m): continue
    v=act(m)
    if v>bv:
        best,bv=m,v; print(bv,','.join(map(str,best)),flush=True)
print('FINAL',bv,','.join(map(str,best)))
