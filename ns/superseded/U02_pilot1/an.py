import sys,re
R={}
for fn in sys.argv[2:]:
    for l in open(fn):
        m=re.search(r'act (-?[0-9.]+).*moves: ([0-9,]+)',l)
        if not m: continue
        R[m.group(2)]=float(m.group(1))
lo,hi=map(int,sys.argv[1].split('-'))
for k,v in sorted(R.items(),key=lambda r:-r[1]):
    mv=[int(x) for x in k.split(',')]
    if not lo<=len(mv)<=hi: continue
    h=[mv.count(c) for c in range(7)]
    print(f"{v:6.3f} {'F' if v>0.696 else '.'} ply{len(mv):02d} last{mv[-1]} lastrow{h[mv[-1]]-1} h={''.join(map(str,h))} {k}")
