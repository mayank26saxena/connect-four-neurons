# single-feature histograms per band: ply bucket and each column height
import sys
lines=sys.stdin.read().split('\n'); band=None; H={}
i=0
while i<len(lines):
    L=lines[i]
    if L.startswith('=== band'): band=L.split()[2].rstrip(':')
    if L.startswith('[pos'):
        rows=list(reversed(lines[i+1:i+7]))
        hs=[sum(1 for r in range(6) if rows[r][c]!='.') for c in range(7)]
        ply=sum(hs)
        H.setdefault(band,{'ply':[], 'h':[[] for _ in range(7)]})
        H[band]['ply'].append(ply)
        for c in range(7): H[band]['h'][c].append(hs[c])
        i+=7; continue
    i+=1
for b in sorted(H):
    d=H[b]; n=len(d['ply'])
    print(b, 'n',n,'mean ply %.1f'%(sum(d['ply'])/n), 'mean heights', ['%.1f'%(sum(x)/n) for x in d['h']])
