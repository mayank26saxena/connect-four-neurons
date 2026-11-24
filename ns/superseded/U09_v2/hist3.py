import sys,re,collections
txt=sys.stdin.read()
blocks=re.findall(r"pole act (-?[\d.]+).*?moves: ([\d,]+)",txt)
C={True:collections.Counter(),False:collections.Counter()};N=collections.Counter()
for a,m in blocks:
    a=float(a);ms=[int(x) for x in m.split(',')];h=[0]*7
    for x in ms[:-1]: h[x]+=1
    F=a>2.0 if len(sys.argv)>1 else a>0.909
    N[F]+=1;C[F][(h[ms[-1]],ms[-1])]+=1
for F in (True,False):
    print(F,N[F],sorted(((k,round(100*v/N[F])) for k,v in C[F].items()),key=lambda x:-x[1])[:15])
