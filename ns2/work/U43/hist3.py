import sys
lines=sys.stdin.read().split('\n')
boards=[]
i=0
while i<len(lines):
    if lines[i].startswith('[pos'):
        boards.append(lines[i+1:i+7]); i+=7
    else: i+=1
n=len(boards)
for H in range(7):
    cnt=[sum(sum(b[r][c]!='.' for r in range(6))==H for c in range(7)) for b in boards]
    print('H=%d'%H,' '.join('%3d'%round(100*cnt.count(k)/n) for k in range(6)))
