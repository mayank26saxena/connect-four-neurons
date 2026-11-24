def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            out.append((l,L[i+1:i+7][::-1]))
    return out
for name,bands in (('lo0-4',range(5)),('hi7-9',range(7,10))):
    S=[x for b in bands for x in parse(f'ns3/work/U22/b{b}.txt')]
    print(name)
    for c in range(7):
        hc=[0]*7
        for l,g in S: hc[sum(1 for r in range(6) if g[r][c]!='.')]+=1
        print('  col',c,hc)
