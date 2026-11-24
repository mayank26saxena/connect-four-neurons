import sys,collections
lines=[l for l in sys.stdin if l.startswith('[pos')]
par=collections.Counter(len(l.split('moves: ')[1].split()[0].split(','))%2 for l in lines)
print('parity (ply odd=1):',dict(par), 'N',len(lines))
for lo,hi in [(4,14),(15,42)]:
    N=0; A=[[0]*7 for _ in range(6)]; B=[[0]*7 for _ in range(6)]
    for l in lines:
        mv=[int(x) for x in l.split('moves: ')[1].split()[0].split(',')]
        if not lo<=len(mv)<=hi: continue
        N+=1; h=[0]*7
        for i,m in enumerate(mv):
            (A if i%2==0 else B)[h[m]][m]+=1; h[m]+=1
    print('ply',lo,hi,'N',N,' cells: first/second player %')
    for r in range(5,-1,-1):
        print(' '.join('%2d/%2d'%(100*A[r][c]//max(N,1),100*B[r][c]//max(N,1)) for c in range(7)))
