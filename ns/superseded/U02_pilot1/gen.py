import random,subprocess,re,json,sys
random.seed(int(sys.argv[1])); N=int(sys.argv[2])
def win(g,r,c,p):
    for dr,dc in((0,1),(1,0),(1,1),(1,-1)):
        n=1
        for s in(1,-1):
            rr,cc=r+dr*s,c+dc*s
            while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: n+=1; rr+=dr*s; cc+=dc*s
        if n>=4: return True
    return False
out=[]
for gi in range(N):
    g=[[0]*7 for _ in range(6)]; h=[0]*7; mv=[]
    L=random.randint(8,40)
    while len(mv)<L:
        cs=[c for c in range(7) if h[c]<6]
        # bias toward center a little
        c=random.choice(cs+[x for x in cs if 2<=x<=4])
        p=len(mv)%2+1; r=h[c]
        g[r][c]=p
        if win(g,r,c,p): g[r][c]=0; 
        else: h[c]+=1; mv.append(c); continue
        cs2=[x for x in cs if x!=c]
        if not cs2: break
        ok=False
        for c in random.sample(cs2,len(cs2)):
            r=h[c]; g[r][c]=p
            if not win(g,r,c,p): h[c]+=1; mv.append(c); ok=True; break
            g[r][c]=0
        if not ok: break
    s=','.join(map(str,mv))
    o=subprocess.run(['uv','run','python','scripts/31_ns_tool.py','act','U02','--moves',s],capture_output=True,text=True).stdout
    acts=[float(m) for m in re.findall(r'after +\d+ moves \([^)]*\): (-?[0-9.]+)',o)]
    out.append({'moves':mv,'acts':acts})
json.dump(out,open(f'ns/work/U02/rand_{sys.argv[1]}.json','w'))
