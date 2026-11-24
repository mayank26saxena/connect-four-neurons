import sys, re, collections
def boards(fn):
    L=open(fn).read().split('\n')
    i=0
    while i<len(L):
        if L[i].startswith('[pos'):
            rows=L[i+1:i+7]
            g=[[{'.':0,'X':1,'O':2}[ch] for ch in rows[5-r]] for r in range(6)]
            ply=len(re.search(r'moves: ([\d,]*)',L[i]).group(1).split(','))
            yield g,ply
            i+=7
        else: i+=1
feat=sys.argv[1]
for b in [0,2,4,5,6,7,8,9]:
    c=collections.Counter()
    for g,ply in boards(f'{REPO}/ns2/work/U75/ex_b{b}.txt'):
        h=[sum(1 for r in range(6) if g[r][cc]) for cc in range(7)]
        if feat=='ply': v=min(ply//4*4,28)
        elif feat.startswith('top'):
            cc=int(feat[3]); v='E' if h[cc]==0 else 'XO'[g[h[cc]-1][cc]-1]
        elif feat.startswith('h'):
            v=h[int(feat[1])]
        c[v]+=1
    print(b, sorted(c.items(), key=lambda x:str(x[0])))
