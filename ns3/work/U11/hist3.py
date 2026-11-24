import sys,re
from collections import Counter
txt=open(sys.argv[1]).read().split('\n')
recs=[];band=None;i=0
while i<len(txt):
    l=txt[i]
    m=re.match(r'=== band (\d)',l)
    if m: band=int(m.group(1))
    m=re.match(r'\[pos \d+\] pole act (\S+)',l)
    if m:
        rows=txt[i+1:i+7]
        g=[[ {'.':0,'X':1,'O':2}[ch] for ch in rows[5-r]] for r in range(6)]
        recs.append((band,g))
    i+=1
W=[-1,0,1,2,1,0,-1]
def feat(g,who): return sum(W[c] for r in range(6) for c in range(7) if g[r][c]==who)
for name,bs in {'lo':[0,1],'b2-4':[2,3,4],'fire':[5,6,7],'top':[8,9]}.items():
    R=[g for b,g in recs if b in bs]
    for f,lab in ((lambda g:feat(g,1),'myCenterW'),(lambda g:feat(g,2),'theirCenterW'),(lambda g:feat(g,1)-feat(g,2),'diff')):
        v=[f(g) for g in R]
        print(name,lab,'mean %.2f'%(sum(v)/len(v)), sorted(Counter(max(-6,min(6,x)) for x in v).items()))
