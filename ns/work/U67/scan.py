# prints grid specs: base with one extra stone of type p at each legal landing cell
import sys
base=sys.argv[1].split('/'); p=sys.argv[2]
rows=[list(r) for r in base[::-1]]
for c in range(7):
    h=sum(1 for r in range(6) if rows[r][c]!='.')
    if h<6:
        g=[r[:] for r in rows]; g[h][c]=p
        print('/'.join(''.join(r) for r in g[::-1]))
