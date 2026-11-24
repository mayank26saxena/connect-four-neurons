import sys,re
def parse(fn):
    L=open(fn).read().split('\n'); out=[]; i=0
    while i<len(L):
        m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+)',L[i])
        if m:
            rows=L[i+1:i+7]; out.append((int(m.group(1)),float(m.group(2)),rows)); i+=7
        else: i+=1
    return out
d={}
for fn in sys.argv[1:]:
    for p,a,r in parse(fn): d[p]=(a,r)
fire=[r for a,r in d.values() if a>0.906 and a>2.0]
non=[r for a,r in d.values() if a<0.4]
print(len(fire),len(non))
for sym in 'XO.':
    print('cell freq',sym,' top(>2) vs low(<0.4)')
    for ri in range(6):
        line=[]
        for c in range(7):
            f=sum(r[ri][c]==sym for r in fire)/len(fire); n=sum(r[ri][c]==sym for r in non)/len(non)
            line.append(f"{f:.2f}/{n:.2f}")
        print(5-ri, ' '.join(line))
