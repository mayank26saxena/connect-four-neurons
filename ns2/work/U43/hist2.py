import sys
lines=sys.stdin.read().split('\n')
boards=[]
i=0
while i<len(lines):
    if lines[i].startswith('[pos'):
        boards.append(lines[i+1:i+7]); i+=7
    else: i+=1
n=len(boards)
print('n',n,'height distribution per column (%), heights 0..6')
for c in range(7):
    hs=[sum(b[r][c]!='.' for r in range(6)) for b in boards]
    print(c,' '.join('%3d'%round(100*hs.count(h)/n) for h in range(7)))
