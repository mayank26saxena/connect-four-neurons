# reads examples output on stdin; prints per-cell frequency of X (me) and O (them) for fired vs not-fired examples
import sys
lines=sys.stdin.read().split('\n')
groups={True:[],False:[]}
i=0
while i<len(lines):
    L=lines[i]
    if L.startswith('[pos'):
        f='FIRES' in L
        rows=lines[i+1:i+7]
        groups[f].append(rows)
        i+=7
    else: i+=1
for f in (True,False):
    g=groups[f]; n=len(g)
    print('fires' if f else 'not', n)
    for ch in 'XO':
        print(' ',ch)
        for r in range(6):
            print('   r%d '%(5-r)+' '.join('%3d'%round(100*sum(b[r][c]==ch for b in g)/max(n,1)) for c in range(7)))
