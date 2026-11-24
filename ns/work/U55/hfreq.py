import sys,re
txt=sys.stdin.read()
blocks=re.findall(r"pole act (-?[\d.]+).*?moves: ([\d,]*)\s.*?\n((?:[.XO]{7}\n){6})",txt)
n=len(blocks)
H=[[0]*7 for _ in range(7)]
T=[[0]*3 for _ in range(7)]
P=[0]*5
blocks=[x for x in blocks if 8<=(len(x[1].split(",")) if x[1] else 0)<=23]; n=len(blocks)
for a,m,g in blocks:
    rows=g.strip().split("\n")[::-1]
    for c in range(7):
        h=sum(1 for r in rows if r[c]!='.')
        H[c][h]+=1
        top='.' if h==0 else rows[h-1][c]
        T[c]['.XO'.index(top)]+=1
    ply=len(m.split(',')) if m else 0
    P[min(4,ply//8)]+=1
print("n",n,"ply/8 dist",[100*x//n for x in P])
for c in range(7):
    print("col",c,"h%",[100*x//n for x in H[c]],"top . X O %",[100*x//n for x in T[c]])
