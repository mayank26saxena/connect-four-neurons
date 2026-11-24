import sys,re,collections
for f in sys.argv[1:]:
    txt=open(f).read()
    recs=re.findall(r"moves: ([\d,]+)\s+last move col (\d)\s+my immediate wins (\[.*?\])\s+must-block (\[.*?\])",txt)
    H=[collections.Counter() for _ in range(7)];last=collections.Counter();mb=collections.Counter();ply=[]
    for mv,lc,w,m in recs:
        mv=[int(x) for x in mv.split(',')]
        for c in range(7): H[c][min(mv.count(c),3)]+=1
        last[int(lc)]+=1
        cols=set(int(x) for x in re.findall(r"\(\d, (\d)\)",m))
        mb['none' if not cols else ''.join(map(str,sorted(cols)))]+=1
        ply.append(len(mv))
    n=len(recs)
    print(f, 'n',n,'meanply',sum(ply)/n)
    print(' P(height==0) by col', [round(H[c][0]/n,2) for c in range(7)])
    print(' last col', sorted(last.items()))
    print(' mustblock', mb.most_common(8))
