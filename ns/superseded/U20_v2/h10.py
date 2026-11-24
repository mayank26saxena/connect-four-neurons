import sys,re
exec(open('h4.py').read().split('P=parse')[0])
H=lambda g,c: sum(g[r][c]!='.' for r in range(6))
P=[p for p in parse(sys.argv[1]) if H(p[0],1)==int(sys.argv[2])]
seen=set()
for g,a,lc,mv in P[:int(sys.argv[3])]:
    if mv in seen: continue
    seen.add(mv); print(a, mv); print('\n'.join(g[::-1]))
