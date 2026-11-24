import sys, re
def boards(fn):
    L = [l.rstrip('\n') for l in open(fn)]
    out = []
    for i, l in enumerate(L):
        if l.startswith('0123456'):
            rows = L[i-6:i]
            out.append(rows)
    return out
for fn in sys.argv[1:]:
    bs = boards(fn)
    n = len(bs)
    print(fn, n, 'theirs (O) fraction per cell, top row first')
    for r in range(6):
        print(' '.join('%3d' % round(100*sum(b[r][c]=='O' for b in bs)/n) for c in range(7)), '   ', ' '.join('%3d' % round(100*sum(b[r][c]=='X' for b in bs)/n) for c in range(7)))
    hs = [[sum(b[r][c] != '.' for r in range(6)) for c in range(7)] for b in bs]
    print('mean heights', ' '.join('%.1f' % (sum(h[c] for h in hs)/n) for c in range(7)))
