import collections
ns={};eval(compile(open('hist2.py').read().split('for b in')[0],'x','exec'),ns)
parse,board=ns['parse'],ns['board']
for b in [0,1,2,3,5,6,7,8,9]:
    c1=collections.Counter();c2=collections.Counter()
    for mv,_,_ in parse(f'b{b}.txt'):
        g,h=board(mv); n=len(mv); them=2-(n%2)  # last mover
        assert g[h[mv[-1]]-1][mv[-1]]==them
        c1[sum(g[r][c]==them for c in (2,4) for r in range(6))]+=1
        c2[sum(g[r][c]==them for c in range(7) for r in range(6))]+=1
    print(b,'O in cols2,4',[c1[k] for k in range(8)])
