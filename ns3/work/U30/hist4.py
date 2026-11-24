import collections
ns={};eval(compile(open('hist2.py').read().split('for b in')[0],'x','exec'),ns)
parse,board=ns['parse'],ns['board']
for b in [0,1,2,3,5,6,7,8,9]:
    rows=collections.Counter(); below=collections.Counter(); prevsame=collections.Counter(); hdiff=collections.Counter()
    for mv,_,_ in parse(f'b{b}.txt'):
        g,h=board(mv); c=mv[-1]; r=h[c]-1
        rows[r]+=1
        below['none' if r==0 else ('same' if g[r-1][c]==g[r][c] else 'opp')]+=1
        prevsame['prevcol=%s'%('same' if mv[-2]==c else 'adj' if abs(mv[-2]-c)==1 else 'far')]+=1
        hdiff[max(h)-min(h)]+=1
    print(b,'row',sorted(rows.items()),dict(below),dict(prevsame),'spread',sorted(hdiff.items()))
