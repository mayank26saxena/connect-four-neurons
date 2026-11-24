ns={};eval(compile(open('hist2.py').read().split('for b in')[0],'x','exec'),ns)
parse,board=ns['parse'],ns['board']
def grids(bs):
    res=[]
    for b in bs:
        for mv,_,_ in parse(f'b{b}.txt'):
            if not (8<=len(mv)<=16): continue
            g,h=board(mv); me=(len(mv)%2)+1
            res.append([[0 if g[r][c]==0 else (1 if g[r][c]==me else 2) for c in range(7)] for r in range(6)])
    return res
hi=grids([7,8,9]); lo=grids([0,1,2])
print(len(hi),len(lo))
for val,name in [(1,'me'),(2,'them')]:
    print(name)
    for r in range(4,-1,-1):
        print(' '.join(f'{100*sum(g[r][c]==val for g in hi)//len(hi):3d}/{100*sum(g[r][c]==val for g in lo)//len(lo):3d}' for c in range(7)))
