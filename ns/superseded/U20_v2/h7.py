import sys,re,collections
exec(open('h4.py').read().split('P=parse')[0])
H=lambda g,c: sum(g[r][c]!='.' for r in range(6))
for fn in sys.argv[1:]:
  P=parse(fn)
  P=[p for p in P if H(p[0],1) in (1,2)]
  print(fn,len(P))
  print(collections.Counter((H(g,1),H(g,1)-H(g,0),H(g,2)-H(g,1)) for g,a,lc,mv in P).most_common(25))
  # landing cell neighbors: cell left (h1,0), right (h1,2), below-left (h1-1,0), below-right (h1-1,2), diag
  def nb(g):
    h=H(g,1)
    f=lambda r,c: g[r][c] if 0<=r<6 and 0<=c<7 else '#'
    return f(h-1,1)+'|'+f(h,0)+f(h,2)+'|'+f(h-1,0)+f(h-1,2)+'|'+f(h+1,0)+f(h+1,2)
  print(collections.Counter(nb(g) for g,a,lc,mv in P).most_common(25))
