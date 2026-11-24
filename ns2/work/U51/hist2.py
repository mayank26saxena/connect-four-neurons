import sys
from collections import Counter
def boards(fn):
    L = [l.rstrip('\n') for l in open(fn)]
    return [L[i-6:i] for i, l in enumerate(L) if l.startswith('0123456')]
for fn in sys.argv[1:]:
    bs = boards(fn)
    hs = [[sum(b[r][c] != '.' for r in range(6)) for c in range(7)] for b in bs]
    print(fn.split('/')[-1], 'h1', sorted(Counter(h[1] for h in hs).items()), ' h2', sorted(Counter(h[2] for h in hs).items()), ' h0', sorted(Counter(h[0] for h in hs).items()))
