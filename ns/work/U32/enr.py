# compare single-cell state frequencies between two example dumps (files argv1 = low, argv2 = high)
import sys
def load(fn):
    lines=open(fn).read().split('\n'); boards=[]
    for i,L in enumerate(lines):
        if L.startswith('[pos'): boards.append(list(reversed(lines[i+1:i+7])))
    return boards
lo=load(sys.argv[1]); hi=load(sys.argv[2])
res=[]
for r in range(5):
    for c in range(7):
        for ch in 'XO.':
            fl=sum(1 for b in lo if b[r][c]==ch)/len(lo); fh=sum(1 for b in hi if b[r][c]==ch)/len(hi)
            res.append((fh-fl,r,c,ch,fl,fh))
res.sort()
for x in res[:15]+[None]+res[-25:]:
    print(x if x is None else '(%d,%d)%s lo %.2f hi %.2f diff %+.2f'%(x[1],x[2],x[3],x[4],x[5],x[0]))
