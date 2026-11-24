import sys,re
txt=sys.stdin.read()
bds=re.findall(r"last move col \d.*?\n((?:[.XO]{7}\n){6})",txt)
n=len(bds)
for ch in "OX":
    print(ch, n)
    for r in range(5,-1,-1):
        print(" ".join("%3d"%(100*sum(1 for b in bds if b.strip().split("\n")[5-r][c]==ch)//n) for c in range(7)))
