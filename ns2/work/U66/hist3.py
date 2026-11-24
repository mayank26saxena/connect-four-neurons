import sys
for l in open(sys.argv[1]):
    bd, mv = l.split()
    ms = [int(x) for x in mv.split(',')]
    h = [0]*7
    for m in ms: h[m] += 1
    if h[2] == 6 and h[3] == 6 and bd in sys.argv[2].split(','):
        print(bd, len(ms), 'me_first' if len(ms)%2==0 else 'me_second', h, 'last', ms[-1])
