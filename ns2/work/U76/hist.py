import sys
# reads examples output on stdin; prints per-cell frequency of mine/theirs and mean heights for the band
lines=sys.stdin.read().split('\n')
boards=[]
i=0
while i<len(lines):
    if lines[i].startswith('[pos'):
        rows=lines[i+1:i+7]
        boards.append(rows); i+=7
    else: i+=1
n=len(boards)
print('n',n)
for ch in 'XO':
    print(ch)
    for r in range(6):
        print(' '.join('%3d'%(100*sum(b[r][c]==ch for b in boards)//max(n,1)) for c in range(7)))
