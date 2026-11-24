import sys
b=sys.argv[1]; L=open(f'ns2/work/U36/ex_b{b}.txt').read().split('\n'); k=0
for i,l in enumerate(L):
    if l.startswith('[pos'):
        rows=L[i+1:i+7]
        if rows[5][4]!='.' and rows[4][4]=='.':
            print(l[:60]); print('\n'.join(rows)); k+=1
            if k>=int(sys.argv[2]): break
