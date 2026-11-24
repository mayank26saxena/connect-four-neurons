import sys
# per-band histogram of single cell states (bottom 3 rows) from examples output
for fn in sys.argv[1:]:
    lines=[l.rstrip('\n') for l in open(fn)]
    boards=[]
    for i,l in enumerate(lines):
        if l.startswith('[pos'):
            rows=lines[i+1:i+7]
            boards.append(rows[::-1])
    n=len(boards)
    print(fn, n)
    for r in range(3):
        out=[]
        for c in range(7):
            cnt={'X':0,'O':0,'.':0}
            for bd in boards: cnt[bd[r][c]]+=1
            out.append("%2d/%2d/%2d"%(cnt['X']*100//n,cnt['O']*100//n,cnt['.']*100//n))
        print(" row%d "%r+"  ".join(out))
