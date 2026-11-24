import collections
rows=[]
for l in open('act4.txt'):
    s,v=l.split(' => '); v=float(v.split()[0]); rows.append((v,[int(x) for x in s.split(',')]))
for c in range(7):
    a=[v for v,mv in rows if c not in mv]; b=[v for v,mv in rows if c in mv]
    print(c,'empty mean %.2f fire%% %.1f | occupied mean %.2f fire%% %.1f'%(sum(a)/len(a),100*sum(x>1.124 for x in a)/len(a),sum(b)/len(b),100*sum(x>1.124 for x in b)/len(b)))
# who owns: mean act by owner of (0,c) me/them
for c in range(7):
    d=collections.defaultdict(list)
    for v,mv in rows:
        o='-'
        for i,x in enumerate(mv):
            if x==c: o='me' if i%2==0 else 'th'; break
        d[o].append(v)
    print(c,{k:'%.2f/%d'%(sum(L)/len(L),len(L)) for k,L in d.items()})
