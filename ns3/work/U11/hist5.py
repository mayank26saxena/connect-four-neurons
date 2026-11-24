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
D=[(0,1),(1,0),(1,1),(1,-1)]
def threats(g,w):
    s=set()
    for r in range(6):
        for c in range(7):
            if g[r][c]: continue
            for dr,dc in D:
                for off in range(-3,1):
                    cells=[(r+(off+k)*dr,c+(off+k)*dc) for k in range(4)]
                    if all(0<=a<6 and 0<=b<7 for a,b in cells) and all(g[a][b]==w for a,b in cells if (a,b)!=(r,c)):
                        s.add((r,c))
    return s
def H(g): return [sum(1 for r in range(6) if g[r][c]) for c in range(7)]
def elev(g,s): h=H(g); return [x for x in s if x[0]>h[x[1]]]
fs={'myT':lambda g:len(threats(g,1)),'theirT':lambda g:len(threats(g,2)),
    'anyT':lambda g:len(threats(g,1)|threats(g,2)),
    'elevAny':lambda g:len(elev(g,threats(g,1)|threats(g,2)))}
for lab,f in fs.items():
  for name,bs in {'lo':[0,1],'b2-4':[2,3,4],'fire':[5,6,7],'top':[8,9]}.items():
    v=[min(f(g),4) for b,g in recs if b in bs]
    print(lab,name,'%.2f'%(sum(v)/len(v)),sorted(Counter(v).items()))
