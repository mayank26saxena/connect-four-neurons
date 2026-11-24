import sys,re
exec_ns={}
src=open('ns2/work/U49/hist2.py').read().split('bands=')[0]
src=src.replace("lines=sys.stdin.read().split('\\n')","lines=LINES")
LINES=sys.stdin.read().split('\n')
g0=globals(); g0['LINES']=LINES
code=compile(src,'h','exec'); 
eval(code,g0)
def f3(mv):
    g,h=grid(mv); lc=mv[-1]; lr=h[lc]-1; f={}
    g[lr][lc]=0
    before_their=wins(g,2); before_my=wins(g,1)
    g[lr][lc]=2
    f['blocked_mywin']=(lr,lc) in before_my
    f['new_theirwins']=min(2,len(wins(g,2)-before_their))
    nb_o=nb_x=0
    for dr in (-1,0,1):
        for dc in (-1,0,1):
            if dr==dc==0: continue
            r,c=lr+dr,lc+dc
            if 0<=r<6 and 0<=c<7:
                nb_o+=g[r][c]==2; nb_x+=g[r][c]==1
    f['nbO']=min(4,nb_o); f['nbX']=min(4,nb_x)
    f['below']=g[lr-1][lc] if lr>0 else 9
    f['above_win']=('my' if (lr+1,lc) in wins(g,1) else '')+('th' if (lr+1,lc) in wins(g,2) else '')
    return f
from collections import Counter
bands=[(-99,0.164),(0.164,0.459),(0.459,1.0),(1.0,99)]
FS=[(a,f3(m)) for a,m in recs]
for k in FS[0][1]:
    print('==',k)
    for lo,hi in bands:
        R=[f[k] for a,f in FS if lo<=a<hi]; C=Counter(R); n=len(R)
        print(f'  {lo:>6}: n={n} '+' '.join(f'{v}:{C[v]*100//n}' for v in sorted(C,key=str)))
