# per-cell histogram (single features) by band, from examples output on stdin
import sys, re
bands = {}
cur = None; rows = []
lines = sys.stdin.read().splitlines()
i = 0
while i < len(lines):
    l = lines[i]
    m = re.match(r'=== band (\d)', l)
    if m: cur = int(m.group(1))
    if l.startswith('[pos'):
        g = lines[i+1:i+7]
        bands.setdefault(cur, []).append(g)
        i += 7; continue
    i += 1
grp = {'low(0-3)': [0,1,2,3], 'fire(5-9)': [5,6,7,8,9]}
for name, bs in grp.items():
    boards = [g for b in bs for g in bands.get(b, [])]
    n = len(boards)
    print(name, n)
    for ch in 'XO.':
        print(' ', ch)
        for r in range(6):
            print('   ', ' '.join('%3d' % round(100*sum(bd[r][c]==ch for bd in boards)/max(n,1)) for c in range(7)))
