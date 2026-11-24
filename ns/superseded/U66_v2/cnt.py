import sys,re,collections
for f in sys.argv[1:]:
    L=open(f).read().split('\n')
    c=collections.Counter(); n=0
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            rows=L[i+1:i+7]; g=[r for r in reversed(rows)]  # g[0]=bottom
            n+=1
            c['O04']+= g[0][4]=='O'
            c['X04']+= g[0][4]=='X'
            c['O00']+= g[0][0]=='O'
            c['O06']+= g[0][6]=='O'
            c['X06']+= g[0][6]=='X'
            m=re.search(r'moves: ([0-9,]*)',l).group(1)
            mv=[int(x) for x in m.split(',')] if m else []
            c['ply_even']+= len(mv)%2==0
            c['ply<8']+= len(mv)<8
            col6=[g[r][6] for r in range(6)]
            c['O_in6>=2']+= col6.count('O')>=2
    print(f,n,{k:round(v/n,2) for k,v in c.items()})
