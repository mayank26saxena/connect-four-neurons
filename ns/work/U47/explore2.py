import re, sys, collections
def parse(fn):
    out=[]
    for line in open(fn):
        m=re.match(r"\[pos (\d+)\] pole act (\S+).*moves: ([\d,]*)",line)
        if m:
            mv=[int(x) for x in m.group(3).split(',') if x!='']
            out.append((float(m.group(2)),mv))
    return out
cells=[(2,0),(3,0),(4,0),(2,2),(3,2),(4,2),(1,2),(1,0),(1,3),(2,3),(3,3),(0,4),(4,4)]
for fn in sys.argv[1:]:
    rows=parse(fn)
    c=collections.Counter(); n=0
    for act,mv in rows:
        h=[0]*7; g={}
        for i,x in enumerate(mv):
            g[(h[x],x)]=i%2; h[x]+=1
        if h[1]!=3: continue
        n+=1
        side=len(mv)%2
        for cl in cells:
            o='E' if cl not in g else ('M' if g[cl]==side else 'T')
            c[(cl,o)]+=1
        c[('ply parity',len(mv)%2)]+=1
        c[('plybin',len(mv)//8)]+=1
    print(fn,n)
    for cl in cells:
        print(' ',cl, {o:round(c[(cl,o)]/n,2) for o in 'EMT'})
    print(' parity', c[('ply parity',0)]/n, ' plybins', [c[('plybin',k)] for k in range(6)])
