import sys,collections
lines=sys.stdin.read().split('\n')
def wins(g,p):
    s=set()
    for r in range(6):
        for c in range(7):
            if g[r][c]!='.': continue
            for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
                cnt=1
                for sgn in (1,-1):
                    k=1
                    while 0<=r+sgn*k*dr<6 and 0<=c+sgn*k*dc<7 and g[r+sgn*k*dr][c+sgn*k*dc]==p: cnt+=1;k+=1
                if cnt>=4: s.add((r,c))
    return s
T=collections.Counter();M=collections.Counter();n=0;nt=0
for i,l in enumerate(lines):
  if l.startswith('[pos'):
    g=lines[i+1:i+7][::-1];n+=1
    t=wins(g,'O'); m=wins(g,'X')
    nt+= bool(t)
    for x in t: T[x]+=1
    for x in m: M[x]+=1
print('n',n,'any their threat',nt)
print('their',T.most_common(8))
print('mine',M.most_common(8))
