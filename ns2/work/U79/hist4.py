import sys, re
txt=sys.stdin.read()
blocks=re.findall(r"moves: ([0-9,]+)\s+last move col (\d)", txt)
H=[0]*7; M=[0]*7; T=[0]*7; ply=0
for mv,lc in blocks:
    mv=[int(x) for x in mv.split(',')]
    n=len(mv); ply+=n
    for i,c in enumerate(mv):
        H[c]+=1
        if (n-1-i)%2==0: T[c]+=1
        else: M[c]+=1
k=len(blocks)
f=lambda a:' '.join('%.1f'%(x/k) for x in a)
print('ply %.1f | H %s | mine %s | theirs %s'%(ply/k,f(H),f(M),f(T)))
