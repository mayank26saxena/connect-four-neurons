import re,collections
C=collections.Counter();F=collections.Counter()
for line in open('ns/work/U09/randacts.txt'):
    m=re.search(r"\(([\d,]+)\): (-?[\d.]+)",line)
    if not m: continue
    ms=[int(x) for x in m.group(1).split(',')];a=float(m.group(2))
    cell=(ms[:-1].count(ms[-1]),ms[-1]);C[cell]+=1;F[cell]+=a>0.909
for k in sorted(C,key=lambda k:-F[k]/C[k]):
    if F[k]: print(k,C[k],F[k])
