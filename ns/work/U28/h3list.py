import re,sys
for f in sys.argv[1:]:
    txt=open(f).read()
    for p,a,mv,bd in re.findall(r"\[pos (\d+)\] pole act ([-\d.]+)\S*\s+(?:FIRES\s+)?moves: (\S*).*?\n((?:[.XO]{7}\n){6})",txt):
        rows=bd.strip().split("\n")[::-1]
        h=sum(1 for r in range(6) if rows[r][0]!='.')
        if h==int(sys.argv[0+0] and H): print(a, mv)
