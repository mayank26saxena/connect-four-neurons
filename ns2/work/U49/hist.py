import sys,re
lines=sys.stdin.read().split('\n')
recs=[]
for i,l in enumerate(lines):
    m=re.match(r'\[pos \d+\] pole act ([-0-9.]+).*moves: ([0-9,]+)',l)
    if m:
        recs.append((float(m.group(1)),list(map(int,m.group(2).split(',')))))
def grid(mv):
    g=[[0]*7 for _ in range(6)]; h=[0]*7; n=len(mv)
    for i,c in enumerate(mv):
        g[h[c]][c]=1 if (i%2)==(n%2) else 2; h[c]+=1
    return g
F=[r for r in recs if r[0]>0.459]; N=[r for r in recs if r[0]<=0.459 and len(r[1])<=18]
print(len(F),len(N))
for who,lab in ((1,'mine'),(2,'theirs')):
    print(lab,'fire% / nonfire%(ply<=18)')
    for r in range(5,-1,-1):
        s=''
        for c in range(7):
            f=sum(grid(m)[r][c]==who for a,m in F)/len(F); n=sum(grid(m)[r][c]==who for a,m in N)/max(1,len(N))
            s+=f' {int(f*100):3d}/{int(n*100):3d}'
        print(s)
