import sys,re
txt=sys.stdin.read()
blocks=re.findall(r"moves: ([0-9,]+).*?\n((?:[.XO]{7}\n){6})",txt)
n=len(blocks)
import collections
for name,cols in [("L012",(0,1,2)),("R456",(4,5,6)),("c2",(2,)),("c1",(1,)),("c4",(4,))]:
    ox=[];
    for mv,g in blocks:
        rows=g.strip().split('\n')[::-1]
        o=sum(rows[r][c]=='O' for r in range(6) for c in cols); x=sum(rows[r][c]=='X' for r in range(6) for c in cols)
        ox.append((o,x))
    print(name,"meanO %.2f meanX %.2f mean(O-X) %.2f"%(sum(a for a,b in ox)/n,sum(b for a,b in ox)/n,sum(a-b for a,b in ox)/n))
