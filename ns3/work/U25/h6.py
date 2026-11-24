import re
from collections import Counter
D={}
for line in open('ex.txt'):
    b=line.split()[0]; m=re.search(r'moves: ([0-9,]+)',line).group(1)
    mv=[int(x) for x in m.split(',')]
    if len(mv)<12: continue
    h=[0]*7
    for c in mv: h[c]+=1
    k='lo' if b in('B0','B1') else 'hi'
    D.setdefault(k,[]).append(h)
for k,v in sorted(D.items()):
    print(k,len(v))
    for c in range(7):
        cnt=Counter(x[c] for x in v); print('  col',c,' '.join('%d:%2d'%(i,round(100*cnt[i]/len(v))) for i in range(7)))
