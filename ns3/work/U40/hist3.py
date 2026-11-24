import sys,re
lines=sys.stdin.read().split('\n')
H={};n=0;i=0
while i<len(lines):
    if lines[i].startswith('[pos'):
        mv=re.search(r'moves: ([0-9,]+)',lines[i]).group(1).split(',')
        i+=7
        if not (4<=len(mv)<=12): continue
        n+=1
        h=[mv.count(str(c)) for c in range(7)]
        for c in range(7):
            k=(c,min(h[c],3)); H[k]=H.get(k,0)+1
    else: i+=1
print('n',n,' rows=height 0,1,2,3+ ; cols 0..6 (%)')
for v in range(4):
    print(v,' '.join('%3d'%(100*H.get((c,v),0)//max(n,1)) for c in range(7)))
