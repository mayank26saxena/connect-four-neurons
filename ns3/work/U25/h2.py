import sys,re
for line in open('ex.txt'):
    b=line.split()[0]
    if b not in sys.argv[1:]: continue
    m=re.search(r'moves: ([0-9,]+)',line).group(1); act=line.split()[4]
    mv=[int(x) for x in m.split(',')]
    if len(mv)<12: continue
    h=[0]*7; g=[[0]*7 for _ in range(6)]
    for i,c in enumerate(mv):
        g[h[c]][c]=1+(i%2); h[c]+=1
    n=len(mv); me=1+(n%2)
    col=lambda c:''.join('.XO'[0 if g[r][c]==0 else (1 if g[r][c]==me else 2)] for r in range(6))
    print(b,act,'h=',''.join(map(str,h)),'c1',col(1),'c2',col(2),'c3',col(3),'last',mv[-1])
