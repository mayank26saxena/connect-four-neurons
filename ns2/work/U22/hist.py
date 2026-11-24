import sys
# reads examples output on stdin, prints per-cell frequency of O and X, and me_first share (by parity)
boards=[];cur=[];plies=[]
for line in sys.stdin:
    line=line.rstrip('\n')
    if line.startswith('[pos'):
        mv=line.split('moves:')[1].split('last')[0].strip()
        plies.append(len(mv.split(',')))
        cur=[]
    elif len(line)==7 and set(line)<=set('.XO'):
        cur.append(line)
        if len(cur)==6: boards.append(cur)
n=len(boards)
print('n',n,'even ply share',sum(p%2==0 for p in plies)/n)
for ch in 'OX':
    print(ch)
    for r in range(6):
        print(' '.join('%3d'%round(100*sum(b[r][c]==ch for b in boards)/n) for c in range(7)))
print('mean heights', [round(sum(sum(b[r][c]!='.' for r in range(6)) for b in boards)/n,2) for c in range(7)])
import collections
for c in (2,3,4):
    print('col',c,'height hist',sorted(collections.Counter(sum(b[r][c]!='.' for r in range(6)) for b in boards).items()))
print('ply hist', sorted(collections.Counter(p//5*5 for p in plies).items()))
