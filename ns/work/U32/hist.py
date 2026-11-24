# reads examples text on stdin; prints single-feature histograms per band: owner of cell (r,c) given by argv
import sys
cells=[(int(a.split(',')[0]),int(a.split(',')[1])) for a in sys.argv[1:]]
lines=sys.stdin.read().split('\n')
band=None; out={}
i=0
while i<len(lines):
    L=lines[i]
    if L.startswith('=== band'): band=L.split()[2].rstrip(':')
    if L.startswith('[pos'):
        g=lines[i+1:i+7]; rows=list(reversed(g))
        for (r,c) in cells:
            ch=rows[r][c]
            out.setdefault((band,(r,c)),{}).setdefault(ch,0)
            out[(band,(r,c))][ch]+=1
        i+=7; continue
    i+=1
for k in sorted(out): print(k, out[k])
