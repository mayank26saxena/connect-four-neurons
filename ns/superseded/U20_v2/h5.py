import sys,re,collections
exec(open('h4.py').read().split('P=parse')[0])
P=parse(sys.argv[1])
H=lambda g,c: sum(g[r][c]!='.' for r in range(6))
for h in range(7):
  c=collections.Counter(''.join(g[r][1] for r in range(6)).rstrip('.') for g,a,lc,mv in P if H(g,1)==h)
  print(h,c.most_common(12))
