import re,sys
txt=open(sys.argv[1]).read().split('\n')
rows=[]
for i,l in enumerate(txt):
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+)',l)
    if m:
        a=float(m.group(2)); grid=txt[i+1:i+7]
        h=[sum(1 for r in grid if r[c]!='.') for c in range(7)]
        rows.append((a,h,grid))
F=[r for r in rows if r[1][1]==6 and r[0]>3.693]; N=[r for r in rows if r[1][1]==6 and r[0]<1.5]
for c in range(7):
    print(c,"fire avg h %.2f full %.2f"%(sum(r[1][c] for r in F)/len(F),sum(r[1][c]==6 for r in F)/len(F)),
      " nonfire avg h %.2f full %.2f"%(sum(r[1][c] for r in N)/len(N),sum(r[1][c]==6 for r in N)/len(N)))
print(len(F),len(N))
# column 1 contents pattern
from collections import Counter
cf=Counter(''.join(r[2][k][1] for k in range(6)) for r in F); cn=Counter(''.join(r[2][k][1] for k in range(6)) for r in N)
print(cf.most_common(8)); print(cn.most_common(8))
