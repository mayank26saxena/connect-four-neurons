import sys,re
txt=sys.stdin.read()
blocks=re.findall(r"moves: ([0-9,]+).*?\n((?:[.XO]{7}\n){6})",txt)
n=len(blocks)
X=[[0]*7 for _ in range(6)];O=[[0]*7 for _ in range(6)]
for mv,g in blocks:
    rows=g.strip().split('\n')[::-1]
    for r in range(6):
        for c in range(7):
            if rows[r][c]=='X':X[r][c]+=1
            if rows[r][c]=='O':O[r][c]+=1
print("n",n)
for r in range(5,-1,-1):
    print(r," ".join("%2d/%2d"%(100*X[r][c]//n,100*O[r][c]//n) for c in range(7)))
