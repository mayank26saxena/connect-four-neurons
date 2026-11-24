import sys, re, collections
col=int(sys.argv[1]); k=int(sys.argv[2])
txt = sys.stdin.read()
blocks = re.split(r'\n(?=\[pos )', txt)
h = collections.Counter()
for bl in blocks:
    if not bl.startswith('[pos'): continue
    rows = bl.split('\n')[1:7]
    g = list(reversed(rows))
    s=''.join(g[r][col] for r in range(6)).rstrip('.')
    h[s[:k]]+=1
print(h.most_common(8))
