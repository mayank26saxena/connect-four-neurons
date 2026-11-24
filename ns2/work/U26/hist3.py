import sys, re
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
    n=len(v)
    print(k,n,'same-col last2 %.2f'%(sum(m[-1]==m[-2] for m in v)/n),
          'col6 nonempty %.2f'%(sum(6 in m for m in v)/n),
          'last=6 %.2f'%(sum(m[-1]==6 for m in v)/n))
