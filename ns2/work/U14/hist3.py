import sys,collections
lines=[l for l in sys.stdin if l.startswith('[pos')]
for lo,hi in [(4,10),(11,20),(21,42)]:
    N=0; H=[0]*7; maxh=collections.Counter(); emp=collections.Counter()
    for l in lines:
        mv=[int(x) for x in l.split('moves: ')[1].split()[0].split(',')]
        if not lo<=len(mv)<=hi: continue
        N+=1; h=[0]*7
        for m in mv: h[m]+=1
        for c in range(7): H[c]+=h[c]
        maxh[max(h)]+=1; emp[h.count(0)]+=1
    if N: print(lo,hi,'N',N,'mean heights',[round(x/N,1) for x in H],'maxh',sorted(maxh.items()),'empty cols',sorted(emp.items()))
