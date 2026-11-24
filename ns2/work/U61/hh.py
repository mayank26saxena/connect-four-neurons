import sys,re
t=sys.stdin.read()
bl=re.findall(r'\[pos \d+\][^\n]*\n((?:[.XO]{7}\n){6})',t)
H=[[0]*7 for _ in range(7)]
for b in bl:
    rows=b.strip().split('\n')
    for c in range(7):
        h=sum(1 for i in range(6) if rows[i][c]!='.')
        H[c][h]+=1
n=len(bl)
for c in range(7): print('col',c,' '.join(f"{H[c][h]*100//n:3d}" for h in range(7)))
