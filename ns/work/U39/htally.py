# per-column height histograms and ply histogram, fired vs not, from examples output on stdin
import sys
lines=sys.stdin.read().split('\n')
G={True:[],False:[]}
i=0
while i<len(lines):
    L=lines[i]
    if L.startswith('[pos'):
        f='FIRES' in L
        rows=lines[i+1:i+7]
        h=[sum(rows[r][c]!='.' for r in range(6)) for c in range(7)]
        G[f].append(h); i+=7
    else: i+=1
for f in (True,False):
    g=G[f]; n=len(g); print('fires' if f else 'not', n)
    for c in range(7):
        print('  col',c,' '.join('%3d'%round(100*sum(h[c]==k for h in g)/n) for k in range(7)))
    pl=[sum(h) for h in g]
    print('  ply', ' '.join('%d-%d:%d'%(a,a+3,sum(a<=p<a+4 for p in pl)) for a in range(0,43,4)))
