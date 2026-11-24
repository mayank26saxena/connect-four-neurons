import sys,re
lines=sys.stdin.read().split('\n')
from collections import Counter
cr=Counter(); rr=Counter(); n=0; ply=Counter()
i=0
while i<len(lines):
    if lines[i].startswith('[pos'):
        b=lines[i+1:i+7]; c=int(re.search(r'last move col (\d)',lines[i]).group(1))
        mv=re.search(r'moves: ([\d,]+)',lines[i]).group(1).split(',')
        h=sum(b[r][c]!='.' for r in range(6)); rr[h-1]+=1; cr[(c,h-1)]+=1; n+=1
        ply[min(len(mv)//5,8)]+=1
        i+=7
    else: i+=1
print('n',n,'last_row',sorted(rr.items()))
print('ply/5',sorted(ply.items()))
for r in range(5,-1,-1):
    print(r,' '.join('%3d'%cr[(c,r)] for c in range(7)))
