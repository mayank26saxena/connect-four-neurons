import re,sys
R,Cc=int(sys.argv[1]),int(sys.argv[2])
for line in open('ns/work/U09/randacts.txt'):
    m=re.search(r"\(([\d,]+)\): (-?[\d.]+)",line)
    if not m: continue
    ms=[int(x) for x in m.group(1).split(',')];a=float(m.group(2))
    if ms[-1]!=Cc or ms[:-1].count(Cc)!=R: continue
    g=[[0]*7 for _ in range(6)];h=[0]*7
    for i,c in enumerate(ms):
        g[h[c]][c]=1 if (len(ms)-i)%2==0 else 2;h[c]+=1
    print(round(a,2),m.group(1))
    for r in range(5,-1,-1): print("".join(".XO"[g[r][c]] for c in range(7)))
