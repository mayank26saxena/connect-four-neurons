import re
exec_src=open('hist2.py').read().split('for b in')[0]
d={}
ns={}
eval(compile(exec_src,'x','exec'),ns)
parse,board=ns['parse'],ns['board']
def grids(bs):
    res=[]
    for b in bs:
        for mv,_,_ in parse(f'b{b}.txt'):
            g,h=board(mv); n=len(mv)
            # convert to me/them: me = player to move = (n%2)+1 in 1/2 encoding
            me=(n%2)+1
            res.append([[0 if g[r][c]==0 else (1 if g[r][c]==me else 2) for c in range(7)] for r in range(6)])
    return res
hi=grids([8,9]); lo=grids([0,1,2])
for val,name in [(1,'me'),(2,'them'),(0,'empty')]:
    print(name,' hi% / lo%')
    for r in range(5,-1,-1):
        print(' '.join(f'{100*sum(g[r][c]==val for g in hi)//len(hi):3d}/{100*sum(g[r][c]==val for g in lo)//len(lo):3d}' for c in range(7)))
