import sys
def board(m):
    g=[[0]*7 for _ in range(6)];h=[0]*7
    for i,c in enumerate(m):
        g[h[c]][c]=1+(i%2); h[c]+=1
    me=1+(len(m)%2)
    return g,h,me
for l in sys.stdin:
    a,mv=l.split()
    m=[int(x) for x in mv.split(',')]
    g,h,me=board(m)
    out=[]
    for c in range(7):
        if h[c]==0: out.append('..');continue
        t=g[h[c]-1][c];k=0;r=h[c]-1
        while r>=0 and g[r][c]==t:k+=1;r-=1
        out.append(('M' if t==me else 'T')+str(k) if h[c]<6 else 'FF')
    print(a.ljust(7),' '.join(out),' last',m[-1])
