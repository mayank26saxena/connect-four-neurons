import sys
from collections import Counter
def board(m):
    g=[[0]*7 for _ in range(6)];h=[0]*7
    for i,c in enumerate(m):
        g[h[c]][c]=1+(i%2); h[c]+=1
    me=1+(len(m)%2)
    return g,h,me
cnt=Counter()
for l in sys.stdin:
    m=[int(x) for x in l.strip().split(',')]
    g,h,me=board(m)
    c=2
    if h[c]==6: cnt['full']+=1; continue
    t=g[h[c]-1][c] if h[c] else 0;k=0;r=h[c]-1
    while r>=0 and g[r][c]==t and t: k+=1;r-=1
    cnt[('M' if t==me else 'T' if t else '-')+str(k)+'h'+str(h[c])]+=1
print(sorted(cnt.items()))
