def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            out.append((l,L[i+1:i+7]))
    return out
for b in range(10):
    S=parse(f'ns3/work/U22/b{b}.txt')
    hs=[[sum(1 for r in range(6) if g[r][c]!='.') for c in range(7)] for _,g in S]
    import_free=0
    h6=sum(h[6] for h in hs)/len(hs); h0=sum(h[0] for h in hs)/len(hs)
    lr=[int(l.split('last move col ')[1][0]) for l,_ in S]
    # height of last-move column
    lh=sum(hs[i][lr[i]] for i in range(len(S)))/len(S)
    full=sum(sum(1 for x in h if x==6) for h in hs)/len(hs)
    print(b, 'h:',' '.join(f'{sum(h[c] for h in hs)/len(hs):.1f}' for c in range(7)), f'lastcolheight {lh:.1f} fullcols {full:.1f}')
