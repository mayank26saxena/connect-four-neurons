import sys
rows=[]
for l in open('act4.txt'):
    s,v=l.split(' => '); v=float(v.split()[0]); rows.append((v,s))
rows.sort(reverse=True)
print('n',len(rows),'fire',sum(v>1.124 for v,_ in rows))
def board(s):
    mv=[int(x) for x in s.split(',')]; g=[['.']*7 for _ in range(6)]; h=[0]*7
    for i,c in enumerate(mv): g[h[c]][c]='X' if i%2==0 else 'O'; h[c]+=1
    return ''.join(g[1])+'/'+''.join(g[0])
k=int(sys.argv[1]) if len(sys.argv)>1 else 40
for v,s in rows[:k]: print('%.2f'%v,s,board(s))
