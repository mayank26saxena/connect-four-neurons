import re,sys
for line in open('ns/work/U09/randacts.txt'):
    m=re.search(r"\(([\d,]+)\): (-?[\d.]+)",line)
    if not m: continue
    ms=[int(x) for x in m.group(1).split(',')];a=float(m.group(2))
    if a<0.909: continue
    g=[[0]*7 for _ in range(6)];h=[0]*7
    for i,c in enumerate(ms):
        g[h[c]][c]=1 if (len(ms)-i)%2==0 else 2;h[c]+=1
    print(round(a,2),"last",(h[ms[-1]]-1,ms[-1]),m.group(1))
    for r in range(5,-1,-1): print("".join(".XO"[g[r][c]] for c in range(7)))
