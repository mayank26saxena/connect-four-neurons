import sys
b=sys.argv[1]; L=open(f'ns2/work/U36/ex_b{b}.txt').read().split('\n'); k=0
cond=sys.argv[3]
for i,l in enumerate(L):
    if l.startswith('[pos'):
        rows=L[i+1:i+7]; g=rows[::-1]
        h=[sum(1 for r in range(6) if g[r][c]!='.') for c in range(7)]
        if eval(cond):
            print(l[:70]); print('\n'.join(rows)); k+=1
            if k>=int(sys.argv[2]): break
