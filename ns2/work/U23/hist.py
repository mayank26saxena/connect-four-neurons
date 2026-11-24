import sys,re
for f in sys.argv[1:]:
    band=None
    for line in open(f):
        m=re.match(r'=== band (\d)',line)
        if m: band=int(m.group(1))
        m=re.search(r'pole act (-?[\d.]+).*moves: ([\d,]+)',line)
        if m:
            a=float(m.group(1)); mv=[int(x) for x in m.group(2).split(',')]
            h=[mv.count(c) for c in range(7)]
            full=sum(x==6 for x in h); 
            print(band, round(a,1), len(mv), 'full',full, 'h',''.join(str(x) for x in h), 'min',min(h), 'last',mv[-1])
