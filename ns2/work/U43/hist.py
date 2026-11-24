import sys,re
# reads examples output on stdin, prints per-cell frequency of O and X (single-cell histogram)
lines=sys.stdin.read().split('\n')
boards=[]
i=0
while i<len(lines):
    if lines[i].startswith('[pos'):
        rows=lines[i+1:i+7]
        boards.append(rows)
        i+=7
    else: i+=1
n=len(boards)
print('n',n)
for ch in 'OX.':
    print('freq',ch)
    for r in range(6):
        print(' '.join('%3d'%round(100*sum(b[r][c]==ch for b in boards)/n) for c in range(7)))
