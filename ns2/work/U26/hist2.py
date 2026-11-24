import sys, re
from collections import Counter
cur=None; d={}
for l in sys.stdin:
    m = re.match(r'=== band (\d)', l)
    if m: cur=int(m.group(1))
    m = re.match(r'\[pos \d+\] pole act \S+.*moves: (\S+)\s+last move col (\d)', l)
    if m:
        mv=m.group(1).split(',')
        d.setdefault('low' if cur<4 else ('fire' if cur>=5 else 'b4'),[]).append((len(mv), int(m.group(2))))
for k,v in d.items():
    print(k, len(v))
    print(' ply', sorted(Counter(min(p//4*4,32) for p,_ in v).items()))
    print(' parity even', sum(p%2==0 for p,_ in v))
    print(' lastcol', sorted(Counter(c for _,c in v).items()))
