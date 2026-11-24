import re
def grid(mv):
    g=[[0]*7 for _ in range(6)];h=[0]*7
    for i,c in enumerate(mv):
        g[h[c]][c]=1 if i%2==len(mv)%2 else 2; h[c]+=1   # 1=mine(to move)
    return g
def stats(bands):
    cnt={};n=0
    for b in bands:
        txt=open(f'ns/work/U39/ex_b{b}.txt').read()
        for a,m in re.findall(r'pole act (-?[\d.]+).*?moves: ([\d,]*)',txt):
            mv=[int(x) for x in m.split(',') if x];g=grid(mv);n+=1
            for r in range(6):
                for c in range(7):
                    cnt[(r,c,g[r][c])]=cnt.get((r,c,g[r][c]),0)+1
    return cnt,n
for name,bands in [('hi',[8,9]),('fire',[5,6,7]),('lo',[0,1,2])]:
    cnt,n=stats(bands);print(name)
    for r in range(5,-1,-1):
        print(' '.join('%2d/%2d'%(100*cnt.get((r,c,1),0)//n,100*cnt.get((r,c,2),0)//n) for c in range(7)))
