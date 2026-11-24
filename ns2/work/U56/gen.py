# build sequences placing given bottom-row colors (relative to the player to move) using fillers
import sys, itertools
# spec: cells "c:v" v in m(me)/t(them); fillers columns list
def build(spec, fill=(6,5,6,5,4)):
    me_cells=[c for c,v in spec if v=='m']; th_cells=[c for c,v in spec if v=='t']
    # choose parity: total stones n = len(me)+len(th)+fillers; mover = me
    for nf in range(0,6):
        n=len(me_cells)+len(th_cells)+nf
        if n<4: continue
        # me is first player if n even
        p1 = me_cells if n%2==0 else th_cells
        p2 = th_cells if n%2==0 else me_cells
        n1=(n+1)//2; n2=n//2
        if len(p1)>n1 or len(p2)>n2: continue
        f1=n1-len(p1); f2=n2-len(p2)
        fl=[6,6,6][:f1] ; fl2=[5,5,5][:f2]
        if f1>3 or f2>3: continue
        a=p1+fl; b=p2+fl2
        seq=[]
        for i in range(n):
            seq.append(a[i//2] if i%2==0 else b[i//2])
        return seq
for arg in sys.argv[1:]:
    spec=[(int(x[0]),x[1]) for x in arg.split(',')]
    print(arg, ','.join(map(str,build(spec))))
