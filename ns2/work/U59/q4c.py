import collections
rows=[]
for l in open('act4.txt'):
    s,v=l.split(' => '); v=float(v.split()[0]); rows.append((v,[int(x) for x in s.split(',')]))
for idx,name in ((3,'last O'),(1,'first O'),(2,'last X'),(0,'first X')):
    d=collections.defaultdict(list)
    for v,mv in rows: d[mv[idx]].append(v)
    print(name,' '.join('%d:%.2f'%(k,sum(L)/len(L)) for k,L in sorted(d.items())))
print('first O x last O mean')
d=collections.defaultdict(list)
for v,mv in rows: d[(mv[1],mv[3])].append(v)
for a in range(7): print(a,' '.join('%5.2f'%(sum(d[(a,b)])/len(d[(a,b)])) for b in range(7)))
print('first X x last X')
d=collections.defaultdict(list)
for v,mv in rows: d[(mv[0],mv[2])].append(v)
for a in range(7): print(a,' '.join('%5.2f'%(sum(d[(a,b)])/len(d[(a,b)])) for b in range(7)))
