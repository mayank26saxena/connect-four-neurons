import sys, re, collections
rows=[]
for line in sys.stdin:
    m=re.search(r'pole act (-?[\d.]+)( FIRES)?\s+moves: ([\d,]+)', line)
    if not m: continue
    a=float(m.group(1)); mv=[int(x) for x in m.group(3).split(',')]
    h=[0]*7
    for c in mv: h[c]+=1
    rows.append((a,len(mv),mv[-1],h[mv[-1]]-1,tuple(h)))
for r in sorted(rows,reverse=True): print("%.3f ply%2d lastcol%d lastrow%d h=%s"%r)
