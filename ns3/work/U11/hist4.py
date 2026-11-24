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
def H(g): return [sum(1 for r in range(6) if g[r][c]) for c in range(7)]
fs={'nEmptyCols':lambda g:sum(h==0 for h in H(g)),
    'maxAdjDiff':lambda g:max(abs(H(g)[c]-H(g)[c+1]) for c in range(6)),
    'maxH':lambda g:max(H(g)),
    'h3':lambda g:H(g)[3],
    'nFullCols':lambda g:sum(h==6 for h in H(g)),
    'range':lambda g:max(H(g))-min(H(g))}
for lab,f in fs.items():
  for name,bs in {'lo':[0,1],'b2-4':[2,3,4],'fire':[5,6,7],'top':[8,9]}.items():
    v=[f(g) for b,g in recs if b in bs]
    print(lab,name,'%.2f'%(sum(v)/len(v)),sorted(Counter(v).items()))
