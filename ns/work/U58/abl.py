# print boards obtained by removing one top X and one top O (parity preserved)
import sys
rows=sys.argv[1].split('/')
g=[list(r) for r in rows[::-1]]
tops=[]
for c in range(7):
    h=sum(1 for r in range(6) if g[r][c]!='.')
    if h: tops.append((h-1,c,g[h-1][c]))
for (r1,c1,p1) in tops:
    if p1!='X': continue
    for (r2,c2,p2) in tops:
        if p2!='O': continue
        h=[list(x) for x in g]; h[r1][c1]='.'; h[r2][c2]='.'
        print('/'.join(''.join(x) for x in h[::-1]), f'-X{r1}{c1}-O{r2}{c2}')
