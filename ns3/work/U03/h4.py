import sys,re,collections
txt=sys.stdin.read()
ms=re.findall(r"moves: ([0-9,]+)",txt)
d=collections.Counter(); e=collections.Counter()
for mv in ms:
    m=[int(x) for x in mv.split(',')]; h=[m.count(c) for c in range(7)]
    d[max(-3,min(3,h[3]-max(h[c] for c in range(7) if c!=3)))]+=1
    e[round(h[3]-sum(h[c] for c in range(7) if c!=3)/6)]+=1
n=len(ms)
print("h3-maxother", sorted((k,round(v/n,2)) for k,v in d.items()))
print("h3-meanother", sorted((k,round(v/n,2)) for k,v in e.items()))
