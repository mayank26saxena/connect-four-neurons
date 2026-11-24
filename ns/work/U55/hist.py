import sys,re,collections
txt=sys.stdin.read()
blocks=re.findall(r"pole act (-?[\d.]+).*?moves: ([\d,]*)\s.*?\n((?:[.XO]{7}\n){6})",txt)
cnt=collections.Counter()
for a,m,g in blocks:
    rows=g.strip().split("\n")
    h=[sum(1 for r in rows if r[c]!='.') for c in range(7)]
    print(a, len(m.split(',')) if m else 0, h, ''.join(rows[5]))
