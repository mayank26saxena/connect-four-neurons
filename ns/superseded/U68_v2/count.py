import sys, re
def parse(fn):
    L=open(fn).read().split("\n"); out=[]
    for i,l in enumerate(L):
        if l.startswith("[pos"):
            a=float(re.search(r"pole act (-?[0-9.]+)",l).group(1))
            rows=L[i+1:i+7]
            g=[[".XO".index(rows[5-r][c]) for c in range(7)] for r in range(6)]
            out.append((a,g,l))
    return out
fire=[x for x in parse(sys.argv[1]) if x[0]>0.349]
non=[x for x in parse(sys.argv[2]) if x[0]<=0.349]
def h(g,c): return sum(1 for r in range(6) if g[r][c])
feats={}
for c in range(7):
    for k in range(4):
        feats[f"h{c}=={k}"]=lambda g,c=c,k=k:h(g,c)==k
for r in range(3):
  for c in range(4):
    for v in (0,1,2):
        feats[f"g{r}{c}=={v}"]=lambda g,r=r,c=c,v=v:g[r][c]==v
res=[]
for n,f in feats.items():
    pf=sum(f(x[1]) for x in fire)/len(fire); pn=sum(f(x[1]) for x in non)/len(non)
    res.append((pf-pn,n,pf,pn))
res.sort()
for r in res[:12]+res[-20:]: print("%-10s fire %.2f non %.2f"%(r[1],r[2],r[3]))
print(len(fire),len(non))
def toprun(g,c):
    k=h(g,c); n=0
    while k-1-n>=0 and g[k-1-n][c]==2: n+=1
    return n
for c in range(7):
  for grp,name in ((fire,"fire"),(non,"non")):
    from collections import Counter
    print(c,name,sorted(Counter(toprun(x[1],c) for x in grp).items()))
