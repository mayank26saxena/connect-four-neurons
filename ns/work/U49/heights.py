# explore helper: print heights for move lists read from stdin (no scoring)
import sys
for line in sys.stdin:
    a, m = line.split()
    h = [0]*7
    mv = [int(x) for x in m.split(',')]
    for c in mv: h[c] += 1
    print(a, len(mv), ''.join(str(x) for x in h), 'last', mv[-1], 'lastrow', h[mv[-1]]-1)
