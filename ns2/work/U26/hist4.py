import sys, re
from collections import Counter
cur=None; d={}
for l in sys.stdin:
    m = re.match(r'=== band (\d)', l)
    if m: cur=int(m.group(1))
    m = re.match(r'\[pos \d+\] pole act \S+.*moves: (\S+)\s+last', l)
    if m:
        mv=[int(x) for x in m.group(1).split(',')]
        k='low' if cur<4 else ('fire' if cur>=5 else 'b4')
        d.setdefault(k,[]).append(mv)
for k,v in d.items():
    n=len(v); print(k,n)
    for c in range(7):
        h=Counter(min(m.count(c),4) for m in v)
        print('  col',c,' '.join('%d:%.2f'%(x,h[x]/n) for x in range(5)))
