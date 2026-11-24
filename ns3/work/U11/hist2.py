import sys,re
from collections import Counter
txt=open(sys.argv[1]).read().split('\n')
recs=[];band=None
for l in txt:
    m=re.match(r'=== band (\d)',l)
    if m: band=int(m.group(1))
    m=re.match(r'\[pos \d+\] pole act (\S+).*moves: (\S+)',l)
    if m: recs.append((band,[int(x) for x in m.group(2).split(',')]))
grp={'lo':[0,1,2],'mid':[3,4],'fire':[5,6,7,8,9]}
for name,bs in grp.items():
    R=[mv for b,mv in recs if b in bs]; n=len(R)
    print(name,n)
    print('  last col',sorted(Counter(m[-1] for m in R).items()))
    print('  prev col',sorted(Counter(m[-2] for m in R).items()))
    print('  me_first(ply even)',sum(len(m)%2==0 for m in R)/n)
    print('  last==prev',sum(m[-1]==m[-2] for m in R)/n, ' last==m[-3]',sum(m[-1]==m[-3] for m in R)/n)
    print('  plyhist',sorted(Counter(min(len(m)//4,8) for m in R).items()))
    def lr(m):
        return m.count(m[-1])-1
    print('  last row',sorted(Counter(lr(m) for m in R).items()))
