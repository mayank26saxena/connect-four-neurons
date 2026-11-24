import sys
from collections import Counter
cnt=Counter()
for line in sys.stdin:
    if not line.startswith('[pos'): continue
    mv=[int(x) for x in line.split('moves: ')[1].split()[0].split(',')]
    cnt[mv[-1]==mv[-2]]+=1
print(dict(cnt))
