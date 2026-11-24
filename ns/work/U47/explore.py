import re, sys, collections
def parse(fn):
    out=[]
    for line in open(fn):
        m=re.match(r"\[pos (\d+)\] pole act (\S+).*moves: ([\d,]*)",line)
        if m:
            mv=[int(x) for x in m.group(3).split(',') if x!='']
            out.append((float(m.group(2)),mv))
    return out
for fn in sys.argv[1:]:
    rows=parse(fn)
    c=collections.Counter()
    for act,mv in rows:
        h=[0]*7
        g={}
        for i,x in enumerate(mv):
            g[(h[x],x)]=i%2; h[x]+=1
        side=len(mv)%2  # player to move parity
        own=lambda r,cc: 'E' if (r,cc) not in g else ('M' if g[(r,cc)]==side else 'T')
        key=(h[1], own(2,1) if h[1]==3 else '-', h[0], mv[-1]==1 if mv else None)
        c[(h[1],)] +=1
        c[('h1=3,top',own(2,1))]+= h[1]==3
        c[('h1=3,h0',h[0])]+= h[1]==3
        c[('h1=3,h2',h[2])]+= h[1]==3
        c[('h1=3,last1',mv[-1]==1)]+= h[1]==3
        c[('h1=3,col1',own(0,1)+own(1,1)+own(2,1))]+= h[1]==3
    print(fn,len(rows))
    for k in sorted(c, key=str): 
        if c[k]: print(' ',k,c[k])
