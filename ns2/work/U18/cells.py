# per-cell histogram (me/them) of example boards read from stdin (examples output)
import sys
boards=[];cur=[]
for line in sys.stdin:
    s=line.rstrip('\n')
    if len(s)==7 and set(s)<=set('.XO'):
        cur.append(s)
        if len(cur)==6:
            if sum(r.count(".") for r in cur) <= 42-int(sys.argv[1]): boards.append(cur)
            cur=[]
n=len(boards)
print("n",n)
for name,ch in (("me X",'X'),("them O",'O')):
    print(name)
    for r in range(6):
        print(' '.join('%3d'%round(100*sum(b[r][c]==ch for b in boards)/n) for c in range(7)))
