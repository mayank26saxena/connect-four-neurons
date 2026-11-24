import sys,re
lines=sys.stdin.read().split('\n')
cnt={};n=0
i=0
while i<len(lines):
    if lines[i].startswith('[pos'):
        rows=lines[i+1:i+7]; n+=1
        for r,row in enumerate(reversed(rows)):
            for c,ch in enumerate(row[:7]):
                cnt[(r,c,ch)]=cnt.get((r,c,ch),0)+1
        i+=7
    else: i+=1
print('n',n)
for ch in 'OX.':
    print(ch)
    for r in range(5,-1,-1):
        print(' '.join('%3d'%(100*cnt.get((r,c,ch),0)//max(n,1)) for c in range(7)))
