# simple per-cell histogram of examples text from stdin: counts per (r,c) of X/O/. 
import sys, re
txt=sys.stdin.read()
blocks=re.findall(r'\[pos \d+\] pole act ([-\d.]+).*?\n((?:[.XO]{7}\n){6})',txt)
n=len(blocks)
cnt={}
for a,g in blocks:
    rows=g.strip().split('\n')
    for i,row in enumerate(rows):
        r=5-i
        for c,ch in enumerate(row):
            cnt.setdefault((r,c),{'X':0,'O':0,'.':0})[ch]+=1
print('n',n)
for r in range(5,-1,-1):
    print(' '.join('%3d/%3d'%(100*cnt[(r,c)]['X']//n,100*cnt[(r,c)]['O']//n) for c in range(7)))
