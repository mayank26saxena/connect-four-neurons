# exploration: per-cell state frequencies (mine/theirs/empty) for move lists on stdin
import sys
N = 0
cnt = {}
for line in sys.stdin:
    a, m = line.split()
    mv = [int(x) for x in m.split(',')]
    g = [[0]*7 for _ in range(6)]
    h = [0]*7
    for i, c in enumerate(mv):
        g[h[c]][c] = i % 2  # 0 = first player
        h[c] += 1
        g[h[c]-1][c] = (i % 2) + 1
    me = len(mv) % 2 + 1  # player to move: 1 if first
    N += 1
    for r in range(6):
        for c in range(7):
            v = g[r][c] if r < h[c] else 0
            s = 'e' if v == 0 else ('m' if v == me else 't')
            cnt[(r, c, s)] = cnt.get((r, c, s), 0) + 1
for s in 'mte':
    print(s)
    for r in reversed(range(6)):
        print(' '.join('%3d' % (100*cnt.get((r, c, s), 0)//N) for c in range(7)))
