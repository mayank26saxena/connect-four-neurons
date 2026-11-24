import sys, re
from collections import Counter
cur=None; d={}
lines=sys.stdin.read().splitlines(); i=0
while i<len(lines):
    l=lines[i]
    m = re.match(r'=== band (\d)', l)
    if m: cur=int(m.group(1))
    if l.startswith('[pos'):
        g=lines[i+1:i+7][::-1]  # g[r] row r
        k='low' if cur<4 else ('fire' if cur>=5 else 'b4')
        d.setdefault(k,[]).append(g); i+=7; continue
    i+=1
for k,v in d.items():
    n=len(v); print(k,n)
    for c in range(7):
        h=Counter()
        for g in v:
            col=[g[r][c] for r in range(6)]
            ht=sum(ch!='.' for ch in col)
            top=col[ht-1] if ht else '-'
            h[top+str(ht)]+=1
        print('  col',c,' '.join('%s:%.2f'%(x,h[x]/n) for x in sorted(h) if h[x]/n>=0.04))
