import sys,re
# single-feature histograms: last move column; height of each column (mean), by hi/lo
band=None; lc={}; hs={}; n={}
for l in sys.stdin:
    m=re.match(r'=== band (\d)',l)
    if m: band=int(m.group(1))
    m=re.search(r'moves: ([\d,]+)',l)
    if m:
        mv=[int(x) for x in m.group(1).split(',')]
        if len(mv)>12: continue
        g='hi' if band>=5 else 'lo'
        n[g]=n.get(g,0)+1
        lc.setdefault(g,[0]*7)[mv[-1]]+=1
        h=[mv.count(c) for c in range(7)]
        hs.setdefault(g,[0]*7)
        for c in range(7): hs[g][c]+=h[c]
for g in n:
    print(g,n[g],'lastcol%',[100*x//n[g] for x in lc[g]],'meanheight',[round(x/n[g],2) for x in hs[g]])
