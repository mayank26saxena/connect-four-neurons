import sys,re
txt=sys.stdin.read()
blocks=re.findall(r"pole act (-?[\d.]+).*?moves: ([\d,]*)\s.*?\n((?:[.XO]{7}\n){6})",txt)
for a,m,g in blocks:
    rows=g.strip().split("\n")[::-1]
    h=[sum(1 for r in rows if r[c]!='.') for c in range(7)]
    th=[sum(1 for r in rows if r[c]=='O') for c in range(7)]
    me=[sum(1 for r in rows if r[c]=='X') for c in range(7)]
    print(a, len(m.split(',')) if m else 0, 'h',h, 'O024', [th[c] for c in (0,2,4)], 'X024',[me[c] for c in (0,2,4)])
