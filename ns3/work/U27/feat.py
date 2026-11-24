import sys
from collections import Counter
def board(m):
    g=[[0]*7 for _ in range(6)];h=[0]*7
    for i,c in enumerate(m):
        g[h[c]][c]=1+(i%2); h[c]+=1
    me=1+(len(m)%2)
    return g,h,me
def toprun(g,h,me,c):
    r=h[c]-1;k=0
    while r>=0 and g[r][c]==me: k+=1;r-=1
    return k if h[c]<6 else -1
col=int(sys.argv[1])
cnt=Counter()
for l in sys.stdin:
    m=[int(x) for x in l.strip().split(',')]
    g,h,me=board(m)
    cnt[toprun(g,h,me,col)]+=1
print(sorted(cnt.items()))
