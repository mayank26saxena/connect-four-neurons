import sys,re
cell=tuple(map(int,sys.argv[1].split(',')))
txt=sys.stdin.read()
for m in re.finditer(r"\[pos \d+\] pole act (\S+).*?moves: (\S+)\s+last move col (\d).*?\n((?:[.XO]{7}\n){6})",txt):
    a,mv,col,bd=m.groups(); col=int(col)
    rows=bd.strip().split("\n")[::-1]
    h=sum(1 for r in rows if r[col]!='.')
    if (h-1,col)==cell:
        print(a,mv); print(bd)
