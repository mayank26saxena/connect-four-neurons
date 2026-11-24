import collections
rows=[]
for l in open('act4.txt'):
    s,v=l.split(' => '); v=float(v.split()[0]); rows.append((v,[int(x) for x in s.split(',')]))
def h(mv):
    H=[0]*7
    for c in mv: H[c]+=1
    return H
# mean act by (col3 empty, col4 empty)
d=collections.defaultdict(list)
for v,mv in rows:
    H=h(mv); d[(H[3]>0,H[4]>0)].append(v)
for k in sorted(d): L=d[k]; print('c3,c4 occupied',k,len(L),'mean %.2f'%(sum(L)/len(L)),'fire%% %.1f'%(100*sum(x>1.124 for x in L)/len(L)))
d=collections.defaultdict(list)
for v,mv in rows:
    H=h(mv); d[tuple(int(H[c]>0) for c in range(7))].append(v)
print('top occupancy patterns by mean:')
for k,L in sorted(d.items(), key=lambda kv:-sum(kv[1])/len(kv[1]))[:15]: print(k,len(L),'%.2f'%(sum(L)/len(L)))
