import sys,re,collections
exec(open('h4.py').read().split('P=parse')[0])
H=lambda g,c: sum(g[r][c]!='.' for r in range(6))
P=parse(sys.argv[1])
P=[p for p in P if H(p[0],1)==2 and H(p[0],0)<2]
P.sort(key=lambda p:-p[1])
for g,a,lc,mv in P[:int(sys.argv[2])]:
    print(a, mv)
    print('\n'.join(g[::-1]))
