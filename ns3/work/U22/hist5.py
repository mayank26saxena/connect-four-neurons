def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            out.append((l,L[i+1:i+7][::-1]))
    return out
for b in range(10):
    S=parse(f'ns3/work/U22/b{b}.txt')
    odd=[0]*8; h5=[0]*8
    for l,g in S:
        hs=[sum(1 for r in range(6) if g[r][c]!='.') for c in range(7)]
        odd[sum(h%2 for h in hs)]+=1
        h5[sum(1 for h in hs if h==5)]+=1
    print(b,'#odd cols',odd,' #h5 cols',h5[:4])
