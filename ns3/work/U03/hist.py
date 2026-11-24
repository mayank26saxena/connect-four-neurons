import sys,re
txt=sys.stdin.read()
blocks=re.findall(r"moves: ([0-9,]+).*?\n((?:[.XO]{7}\n){6})",txt)
n=len(blocks); hs=[[0]*8 for _ in range(7)]; ply=[]
for mv,g in blocks:
    m=[int(x) for x in mv.split(',')]
    h=[m.count(c) for c in range(7)]
    for c in range(7): hs[c][min(h[c],7)]+=1
    ply.append(len(m))
print("n",n,"ply mean %.1f"%(sum(ply)/n))
for c in range(7): print(c,"h0=%.2f"%(hs[c][0]/n),"mean=%.2f"%(sum(k*hs[c][k] for k in range(8))/n))
