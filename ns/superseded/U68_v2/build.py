import sys
# args: column strings bottom-up, e.g. XO O XXO - - - -   (X = player to move at end)
cols=[("" if s=="-" else s) for s in sys.argv[1:8]]
nx=sum(s.count("X") for s in cols); no=sum(s.count("O") for s in cols)
if nx==no: first="X"
elif no==nx+1: first="O"
else: print("bad counts",nx,no); sys.exit(1)
def wins(cols):
    g=[[c[r] if r<len(c) else "." for c in cols] for r in range(6)]
    for r in range(6):
        for c in range(7):
            p=g[r][c]
            if p==".": continue
            for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
                if all(0<=r+k*dr<6 and 0<=c+k*dc<7 and g[r+k*dr][c+k*dc]==p for k in range(4)): return True
    return False
total=nx+no
def dfs(h,seq,turn):
    if len(seq)==total: return seq
    for c in range(7):
        if h[c]<len(cols[c]) and cols[c][h[c]]==turn:
            h2=h[:]; h2[c]+=1
            cur=[cols[i][:h2[i]] for i in range(7)]
            if len(seq)+1<total and wins(cur): continue
            r=dfs(h2,seq+[c],"O" if turn=="X" else "X")
            if r: return r
    return None
r=dfs([0]*7,[], first)
print(",".join(map(str,r)) if r else "none")
