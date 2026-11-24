import sys,re
def load(f):
    txt=open(f).read()
    blocks=re.findall(r"moves: ([0-9,]+).*?\n((?:[.XO]{7}\n){6})",txt)
    P={k:[[0]*7 for _ in range(6)] for k in 'XO.'}
    for mv,g in blocks:
        rows=g.strip().split('\n')[::-1]
        for r in range(6):
            for c in range(7): P[rows[r][c]][r][c]+=1/len(blocks)
    return P,len(blocks)
hi,nh=load(sys.argv[1]); lo,nl=load(sys.argv[2])
print(nh,nl)
for k in 'XO.':
    print("==",k,"(hi-lo)*100")
    for r in range(5,-1,-1): print(r," ".join("%+4d"%round(100*(hi[k][r][c]-lo[k][r][c])) for c in range(7)))
