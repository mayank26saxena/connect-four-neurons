import sys, re, collections
txt = sys.stdin.read()
blocks = re.split(r'\n(?=\[pos )', txt)
H = [collections.Counter() for _ in range(7)]
for bl in blocks:
    if not bl.startswith('[pos'): continue
    rows = bl.split('\n')[1:7]
    grid = list(reversed(rows))
    for c in range(7):
        h = sum(1 for r in range(6) if grid[r][c] != '.')
        H[c][h] += 1
for c in range(7):
    print(' col',c, [H[c][h] for h in range(7)])
