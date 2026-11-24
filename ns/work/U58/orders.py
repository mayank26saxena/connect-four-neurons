import sys, random
rows=sys.argv[1].split('/')[::-1]; N=int(sys.argv[2])
cols=[[rows[r][c] for r in range(6) if rows[r][c]!='.'] for c in range(7)]
out=set()
def rec(cols,turn,seq):
    if len(out)>=N*20: return
    if all(not c for c in cols): out.add(','.join(map(str,seq[::-1]))); return
    cs=list(range(7)); random.shuffle(cs)
    for c in cs:
        if cols[c] and cols[c][-1]==turn:
            k=[list(x) for x in cols]; k[c].pop(); rec(k,'X' if turn=='O' else 'O',seq+[c])
random.seed(0); rec(cols,'O',[])
for s in random.sample(sorted(out),min(N,len(out))): print(s)
