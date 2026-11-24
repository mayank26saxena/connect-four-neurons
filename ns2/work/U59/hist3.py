import re
seen=set(); data={}
for l in open('ex.txt'):
    b=l.split()[0]; m=re.search(r'moves: (\S+)',l).group(1)
    if (b,m) in seen: continue
    seen.add((b,m))
    mv=[int(x) for x in m.split(',')]
    if len(mv)<12: continue
    g=[[0]*7 for _ in range(6)]; h=[0]*7; n=len(mv)
    for i,c in enumerate(mv):
        g[h[c]][c]=1 if i%2==n%2 else 2; h[c]+=1
    key='F' if b in('B7','B8','B9') else 'N'
    data.setdefault(key,[]).append((g,h,n))
for k in data:
    L=data[k];N=len(L)
    print(k,N,'ply %.1f'%(sum(x[2] for x in L)/N),'heights',[round(sum(x[1][c] for x in L)/N,1) for c in range(7)])
    print('  rel heights (h/ply*7)',[round(sum(x[1][c]/x[2]*7 for x in L)/N,2) for c in range(7)])
    for who in (1,2):
        print('  ', 'me' if who==1 else 'them')
        for r in range(5,-1,-1): print('    ',' '.join('%3d'%round(100*sum(x[0][r][c]==who for x in L)/N) for c in range(7)))
