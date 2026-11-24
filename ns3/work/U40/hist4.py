import sys,re
H={};n=0
for line in sys.stdin:
    if line.startswith('[pos'):
        mv=re.search(r'moves: ([0-9,]+)',line).group(1).split(',')
        if len(mv)<28: continue
        n+=1
        h=[mv.count(str(c)) for c in range(7)]
        k=min(h[1],h[2],h[3]); H[k]=H.get(k,0)+1
print('n',n,'min height cols1-3 dist:',sorted(H.items()))
