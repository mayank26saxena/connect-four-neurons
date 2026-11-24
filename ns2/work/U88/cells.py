from collections import Counter
def load(bds):
    G=[]
    for bd in bds:
        L=open(f'ns2/work/U88/ex_b{bd}.txt').read().split('\n')
        for i,l in enumerate(L):
            if l.startswith('[pos'):
                rows=L[i+1:i+7]; G.append([[{'.':0,'X':1,'O':2}[ch] for ch in rows[5-r]] for r in range(6)])
    return G
hi=load([7,8,9]); lo=load([0,1,2])
for s,name in ((1,'me'),(2,'them'),(0,'empty')):
    print(name, 'frac high - frac low (x100)')
    for r in range(5,-1,-1):
        print(' '.join(f'{100*(sum(g[r][c]==s for g in hi)/len(hi)-sum(g[r][c]==s for g in lo)/len(lo)):+5.0f}' for c in range(7)))
