import sys
lines=sys.stdin.read().split('\n')
boards=[]
i=0
while i<len(lines):
    if lines[i].startswith('[pos'):
        boards.append(lines[i+1:i+7]); i+=7
    else: i+=1
from collections import Counter
hs=[]
for b in boards:
    h=[sum(b[r][c]!='.' for r in range(6)) for c in range(7)]
    hs.append(h)
n=len(hs)
print('mean heights', [round(sum(h[c] for h in hs)/n,1) for c in range(7)])
print('col2 height hist', sorted(Counter(h[2] for h in hs).items()))
print('h3-h2 hist', sorted(Counter(h[3]-h[2] for h in hs).items()))
print("h1",sorted(Counter(h[1] for h in hs).items()),"h4",sorted(Counter(h[4] for h in hs).items()))
