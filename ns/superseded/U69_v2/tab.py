import re,sys
txt=open(sys.argv[1]).read().split('\n')
rows=[]
for i,l in enumerate(txt):
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+)',l)
    if m:
        a=float(m.group(2)); grid=txt[i+1:i+7]
        h=[sum(1 for r in grid if r[c]!='.') for c in range(7)]
        ply=sum(h); legal=[c for c in range(7) if h[c]<6]
        rows.append((a,ply,h,legal))
rows.sort()
for a,ply,h,legal in rows:
    if a>2 or (len(legal)<=2):
        print(f"{a:7.2f} ply{ply:3d} h{h} nleg{len(legal)} {legal}")
