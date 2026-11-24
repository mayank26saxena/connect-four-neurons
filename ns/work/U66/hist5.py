import sys, re, collections
txt = sys.stdin.read()
blocks = re.split(r'\n(?=\[pos )', txt)
h = collections.Counter()
for bl in blocks:
    if not bl.startswith('[pos'): continue
    rows = bl.split('\n')[1:7]
    g = list(reversed(rows))
    hs=[sum(1 for r in range(6) if g[r][c]!='.') for c in range(7)]
    h[hs[4]]+=1
print(sorted(h.items()))
