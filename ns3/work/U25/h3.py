import re
from collections import Counter
D={}
for line in open('ex.txt'):
    b=line.split()[0]; m=re.search(r'moves: ([0-9,]+)',line).group(1)
    mv=[int(x) for x in m.split(',')]
    h=[0]*7; g=[[0]*7 for _ in range(6)]
    for i,c in enumerate(mv):
        g[h[c]][c]=1+(i%2); h[c]+=1
    me=1+(len(mv)%2)
    top=['.' if h[c]==0 else ('X' if g[h[c]-1][c]==me else 'O') for c in range(7)]
    k='lo' if b in('B0','B1') else 'hi'
    D.setdefault(k,[]).append((top,h))
for k,v in D.items():
    print(k,len(v))
    for c in range(7):
        cnt=Counter(t[c] for t,h in v); print(' col',c,'top',{x:round(100*cnt[x]/len(v)) for x in '.XO'}, 'meanh',round(sum(h[c] for t,h in v)/len(v),2))
