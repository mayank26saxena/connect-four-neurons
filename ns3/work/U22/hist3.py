def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            out.append((l,L[i+1:i+7][::-1]))  # g[r] r=0 bottom
    return out
for b in range(10):
    S=parse(f'ns3/work/U22/b{b}.txt')
    lr={};under={};h6={}
    for l,g in S:
        c=int(l.split('last move col ')[1][0]); r=max(r for r in range(6) if g[r][c]!='.')
        lr[r]=lr.get(r,0)+1
        u='floor' if r==0 else g[r-1][c]
        under[u]=under.get(u,0)+1
        h=sum(1 for r in range(6) if g[r][6]!='.'); h6[h]=h6.get(h,0)+1
    print(b,'lastrow',dict(sorted(lr.items())),'under',under,'h6',dict(sorted(h6.items())))
