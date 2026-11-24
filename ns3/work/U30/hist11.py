import collections
ns={};eval(compile(open('hist2.py').read().split('for b in')[0],'x','exec'),ns)
parse,board=ns['parse'],ns['board']
def pairs(g,p,dirs):
    n=0
    for r in range(6):
        for c in range(7):
            if g[r][c]!=p: continue
            for dr,dc in dirs:
                rr,cc=r+dr,c+dc
                if 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: n+=1
    return n
for b in [0,1,2,3,5,6,7,8,9]:
    a=collections.Counter(); m=collections.Counter()
    for mv,_,_ in parse(f'b{b}.txt'):
        g,h=board(mv); them=2-(len(mv)%2); k=sum(1 for x in g for y in x if y==them)
        p=pairs(g,them,[(0,1),(1,1),(1,-1)])
        a[min(int(4*p/max(k,1)),6)]+=1
        m[min(int(4*pairs(g,3-them,[(0,1),(1,1),(1,-1)])/max(k,1)),6)]+=1
    print(b,'their nonvert pairs per stone x4',[a[i] for i in range(7)],' mine',[m[i] for i in range(7)])
