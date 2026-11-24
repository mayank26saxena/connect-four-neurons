import re,sys,collections
def parse(fn):
    out=[]
    for line in open(fn):
        m=re.search(r'moves: ([\d,]+)\s+last move col (\d)',line)
        if m:
            mv=[int(x) for x in m.group(1).split(',')]
            out.append(mv)
    return out
for b in [0,1,2,3,5,6,7,8,9]:
    gs=parse(f'b{b}.txt')
    lc=collections.Counter(g[-1] for g in gs)
    ply=sorted(len(g) for g in gs)
    H=[[0]*7 for _ in gs]
    hz=[0]*7
    for i,g in enumerate(gs):
        for c in g: H[i][c]+=1
        for c in range(7):
            if H[i][c]==0: hz[c]+=1
    par=collections.Counter(len(g)%2 for g in gs)
    print(b,'n',len(gs),'medply',ply[len(ply)//2],'lastcol',[lc[c] for c in range(7)],'emptycol',hz,'parity',dict(par))
