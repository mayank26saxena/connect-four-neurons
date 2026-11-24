import sys,re
txt=sys.stdin.read()
blocks=re.findall(r"pole act (-?[\d.]+).*?moves: ([\d,]*)\s.*?\n((?:[.XO]{7}\n){6})",txt)
n=len(blocks)
F={'X':[[0]*7 for _ in range(6)],'O':[[0]*7 for _ in range(6)]}
for a,m,g in blocks:
    rows=g.strip().split("\n")
    for r in range(6):
        for c in range(7):
            ch=rows[r][c]
            if ch in F: F[ch][r][c]+=1
print("n",n)
for k in 'XO':
    print(k)
    for r in range(6):
        print(' '.join('%3d'%(100*F[k][r][c]//n) for c in range(7)))
