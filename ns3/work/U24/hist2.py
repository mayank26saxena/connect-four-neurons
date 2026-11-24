import sys,re,collections
for fn in sys.argv[1:]:
    L=open(fn).read().split('\n')
    lc=collections.Counter(); h=[collections.Counter() for _ in range(7)]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            lc[int(re.search(r'last move col (\d)',l).group(1))]+=1
            g=L[i+1:i+7]
            for c in range(7):
                h[c][sum(g[r][c]!='.' for r in range(6))]+=1
    print(fn,'lastcol',sorted(lc.items()))
    for c in range(7): print('  h%d'%c,[h[c][k] for k in range(7)])
