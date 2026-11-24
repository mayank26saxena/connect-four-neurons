import re
seen=set(); data={}
for l in open('ex.txt'):
    b=l.split()[0]; m=re.search(r'moves: (\S+)',l).group(1)
    if (b,m) in seen: continue
    seen.add((b,m))
    mv=[int(x) for x in m.split(',')]
    g=[[-1]*7 for _ in range(6)]; h=[0]*7
    for i,c in enumerate(mv):
        g[h[c]][c]=i%2; h[c]+=1
    n=len(mv); me=n%2
    def wins(p):
        s=set()
        for r in range(6):
            for c in range(7):
                if g[r][c]!=-1: continue
                for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
                    cnt=0
                    for sgn in (1,-1):
                        k=1
                        while 0<=r+sgn*k*dr<6 and 0<=c+sgn*k*dc<7 and g[r+sgn*k*dr][c+sgn*k*dc]==p: cnt+=1;k+=1
                    if cnt>=3: s.add((r,c))
        return s
    data.setdefault(b,[]).append((wins(me),wins(1-me)))
for b in sorted(data):
    L=data[b];N=len(L)
    print(b,N,'any mine %.2f any theirs %.2f'%(sum(1 for x in L if x[0])/N,sum(1 for x in L if x[1])/N))
    for k,name in ((0,'my'),(1,'their')):
        print(' ',name)
        for r in range(5,-1,-1):
            print('   ',' '.join('%3d'%round(100*sum((r,c) in x[k] for x in L)/N) for c in range(7)))
