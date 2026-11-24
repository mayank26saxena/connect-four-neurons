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
def frac_outer(g,w):
    t=[c for r in range(6) for c in range(7) if g[r][c]==w]
    return sum(c in (0,1,5,6) for c in t)/max(1,len(t))
def mycenter(g): return sum(1 for r in range(6) for c in (2,3,4) if g[r][c]==1)
def theircenter(g): return sum(1 for r in range(6) for c in (2,3,4) if g[r][c]==2)
for lab,f in {'myOuterFrac':lambda g:round(frac_outer(g,1),1),'theirOuterFrac':lambda g:round(frac_outer(g,2),1),'myC-theirC':lambda g:mycenter(g)-theircenter(g)}.items():
  for name,bs in {'lo':[0,1],'b2-4':[2,3,4],'fire':[5,6,7],'top':[8,9]}.items():
    v=[f(g) for b,g in recs if b in bs]
    print(lab,name,'%.2f'%(sum(v)/len(v)),sorted(Counter(v).items()))
