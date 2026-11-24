import sys,re
# annotate act output with heights
for line in sys.stdin:
    m=re.search(r'after\s+(\d+) moves \(([\d,]*)\): (-?[\d.]+)',line)
    if m and m.group(2):
        mv=[int(x) for x in m.group(2).split(',')]
        h=''.join(str(mv.count(c)) for c in range(7))
        print(m.group(1), h, m.group(3))
