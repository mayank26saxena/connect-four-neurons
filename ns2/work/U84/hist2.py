import sys
def parse(f):
    L=open(f).read().split('\n');out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            rows=L[i+1:i+7]; mv=l.split('moves: ')[1].split()[0]; out.append((rows[::-1],mv))
    return out
for f in sys.argv[1:]:
    bs=parse(f); n=len(bs)
    print(f)
    for c in range(7):
        hist=[0]*7
        for b,_ in bs: hist[sum(b[r][c]!='.' for r in range(6))]+=1
        print('  col',c,'height hist',hist)
    lc=[0]*7
    for b,mv in bs: lc[int(mv.split(',')[-1])]+=1
    print('  last col',lc)
    pl=[0]*43
    for b,mv in bs: pl[len(mv.split(','))]+=1
    print('  ply', [ (i,p) for i,p in enumerate(pl) if p])
