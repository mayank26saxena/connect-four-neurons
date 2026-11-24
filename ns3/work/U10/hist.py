import sys,re,collections
txt=sys.stdin.read()
h=[collections.Counter() for _ in range(7)]; lc=collections.Counter(); n=0; ply=[]
for m in re.finditer(r"moves: ([\d,]+)",txt):
    mv=[int(x) for x in m.group(1).split(",")]; n+=1
    for c in range(7): h[c][mv.count(c)]+=1
    lc[mv[-1]]+=1; ply.append(len(mv))
print("n",n,"mean ply",sum(ply)/max(n,1))
for c in range(7): print("col",c,"height dist",sorted(h[c].items()))
print("last col",sorted(lc.items()))
