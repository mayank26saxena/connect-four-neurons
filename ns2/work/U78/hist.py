import sys,re
txt=sys.stdin.read()
blocks=re.findall(r"last move col (\d).*?\n((?:[.XO]{7}\n){6})",txt)
from collections import Counter
c=Counter()
for col,bd in blocks:
    rows=bd.strip().split("\n")[::-1]
    col=int(col)
    h=sum(1 for r in rows if r[col]!='.')
    c[(col,h-1)]+=1
print(sorted(c.items(),key=lambda x:-x[1])[:15])
