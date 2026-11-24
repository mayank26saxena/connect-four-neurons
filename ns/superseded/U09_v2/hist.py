import sys,re
txt=sys.stdin.read()
blocks=re.findall(r"pole act (-?[\d.]+).*?\n((?:[.XO]{7}\n){6})",txt)
fire=[[0]*7 for _ in range(6)];fx=[[0]*7 for _ in range(6)];nf=0
non=[[0]*7 for _ in range(6)];nx=[[0]*7 for _ in range(6)];nn=0
for a,g in blocks:
    a=float(a);rows=g.split()[::-1]
    F=a>0.909
    if F: nf+=1
    else: nn+=1
    for r in range(6):
        for c in range(7):
            ch=rows[r][c]
            if ch=='O': (fire if F else non)[r][c]+=1
            if ch=='X': (fx if F else nx)[r][c]+=1
print("fire",nf,"non",nn)
for name,A,n in [("O fire",fire,nf),("O non",non,nn),("X fire",fx,nf),("X non",nx,nn)]:
    print(name)
    for r in range(5,-1,-1): print(" ".join("%3d"%(100*A[r][c]//max(n,1)) for c in range(7)))
