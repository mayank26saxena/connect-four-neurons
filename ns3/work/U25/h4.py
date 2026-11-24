import re,sys
from collections import Counter
C=int(sys.argv[1])
D={}
for line in open('ex.txt'):
    b=line.split()[0]; m=re.search(r'moves: ([0-9,]+)',line).group(1)
    mv=[int(x) for x in m.split(',')]
    h=[0]*7; g=[[0]*7 for _ in range(6)]
    for i,c in enumerate(mv):
        g[h[c]][c]=1+(i%2); h[c]+=1
    me=1+(len(mv)%2)
    if h[C]>=6: continue
    r0=h[C]
    feats={}
    for dr in (1,0,-1,-2):
        for dc in (-3,-2,-1,0,1,2,3):
            r,c=r0+dr,C+dc
            v='#' if not(0<=r<6 and 0<=c<7) else ('.' if g[r][c]==0 else ('X' if g[r][c]==me else 'O'))
            feats[(dr,dc)]=v
    k='lo' if b in('B0','B1') else 'hi'
    D.setdefault(k,[]).append(feats)
for k,v in sorted(D.items()):
    print(k,len(v))
    for dr in (1,0,-1,-2):
        print('  ',' '.join('%s' % ''.join('%s%2d'%(x,round(100*sum(f[(dr,dc)]==x for f in v)/len(v))) for x in 'XO') for dc in (-3,-2,-1,0,1,2,3)))
