import sys,re
def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            g=L[i+1:i+7]; out.append((l,g))
    return out
lo=[];hi=[]
for b in range(10):
    (hi if b>=5 else lo).extend(parse(f'ns3/work/U22/b{b}.txt'))
for name,S in (('lo',lo),('hi',hi)):
    print(name,len(S))
    for ch in 'XO.':
        print(' ',ch)
        for r in range(6):
            row=[sum(1 for _,g in S if g[r][c]==ch)*100//len(S) for c in range(7)]
            print('   row',5-r,' '.join(f'{v:3d}' for v in row))
