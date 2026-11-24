import sys,re
for line in sys.stdin:
    m=re.search(r'pole act (\S+).*moves: ([\d,]*)',line)
    if m:
        mv=[int(x) for x in m.group(2).split(',') if x!='']
        h=[mv.count(c) for c in range(7)]
        if h[2] not in (2,3): continue
        me = len(mv)%2  # player index to move: 0 = P1
        col=[ 'X' if (i%2)==me else 'O' for i,c in enumerate(mv) if c==2]
        print(m.group(1), 'ply',len(mv),'h',h, 'col2',''.join(col))
