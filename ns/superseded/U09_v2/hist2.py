import sys,re
txt=sys.stdin.read()
blocks=re.findall(r"pole act (-?[\d.]+).*?\n((?:[.XO]{7}\n){6})",txt)
D=[(0,1),(1,0),(1,1),(1,-1)]
def threats(g,p):
    out=set()
    for r in range(6):
        for c in range(7):
            if g[r][c]!='.':continue
            for dr,dc in D:
                n=1
                for s in (1,-1):
                    k=1
                    while 0<=r+s*k*dr<6 and 0<=c+s*k*dc<7 and g[r+s*k*dr][c+s*k*dc]==p: n+=1;k+=1
                if n>=4: out.add((r,c))
    return out
cnt={True:[[0]*7 for _ in range(6)],False:[[0]*7 for _ in range(6)]};N={True:0,False:0}
anyc={True:0,False:0}
for a,g in blocks:
    a=float(a);rows=g.split()[::-1];F=a>0.909;N[F]+=1
    t=threats(rows,'O')
    if t: anyc[F]+=1
    for r,c in t: cnt[F][r][c]+=1
print(N,anyc)
for F in (True,False):
    print("fire" if F else "non")
    for r in range(5,-1,-1): print(" ".join("%3d"%(100*cnt[F][r][c]//N[F]) for c in range(7)))
