import collections
ns={};eval(compile(open('hist2.py').read().split('for b in')[0],'x','exec'),ns)
parse,board=ns['parse'],ns['board']
D=[(0,1),(1,0),(1,1),(1,-1)]
def wins(g,p):
    s=set()
    for r in range(6):
        for c in range(7):
            if g[r][c]: continue
            for dr,dc in D:
                n=1
                for sgn in (1,-1):
                    rr,cc=r+sgn*dr,c+sgn*dc
                    while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: n+=1; rr+=sgn*dr; cc+=sgn*dc
                if n>=4: s.add((r,c))
    return s
for b in [0,1,2,3,5,6,7,8,9]:
    tw=collections.Counter(); mw=collections.Counter()
    for mv,_,_ in parse(f'b{b}.txt'):
        g,h=board(mv); them=2-(len(mv)%2); me=3-them
        tw[min(len(wins(g,them)),3)]+=1; mw[min(len(wins(g,me)),3)]+=1
    print(b,'their threat cells',[tw[k] for k in range(4)],'my',[mw[k] for k in range(4)])
