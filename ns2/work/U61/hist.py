import sys,re
# reads examples output on stdin, prints per-cell X/O fraction grid
txt=sys.stdin.read()
blocks=re.findall(r'\[pos \d+\][^\n]*\n((?:[.XO]{7}\n){6})',txt)
n=len(blocks); X=[[0]*7 for _ in range(6)]; O=[[0]*7 for _ in range(6)]
for b in blocks:
    rows=b.strip().split('\n')
    for i,row in enumerate(rows):
        r=5-i
        for c,ch in enumerate(row):
            if ch=='X': X[r][c]+=1
            if ch=='O': O[r][c]+=1
print('n',n)
for r in range(5,-1,-1):
    print(' '.join(f"{X[r][c]*100//max(n,1):3d}/{O[r][c]*100//max(n,1):<3d}" for c in range(7)))
