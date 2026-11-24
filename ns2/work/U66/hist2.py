import sys
by = {}
for l in open(sys.argv[1]):
    bd, mv = l.split()
    ms = [int(x) for x in mv.split(',')]
    h = [0]*7
    for m in ms: h[m] += 1
    by.setdefault(bd, []).append(h)
for bd in sorted(by):
    L = by[bd]; n = len(L)
    k = [sum((x[2] == 6) + (x[3] == 6) == j for x in L) for j in range(3)]
    nf = [sum(sum(c == 6 for c in x) == j for x in L) for j in range(7)]
    print(bd, 'n full of {2,3}:', k, ' total full cols hist:', nf)
