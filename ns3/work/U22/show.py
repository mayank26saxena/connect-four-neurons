import sys
def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            out.append((l,L[i+1:i+7]))
    return out
S=[x for b in sys.argv[1:] for x in parse(f'ns3/work/U22/b{b}.txt')]
S=[x for x in S if len(x[0].split('moves: ')[1].split()[0].split(','))<=12]
for k in range(0,len(S),6):
    grp=S[k:k+6]
    print('   '.join(l.split()[3]+' '+l.split('moves: ')[1].split()[0][:18].ljust(18) for l,_ in grp))
    for r in range(6):
        if all(g[r]=='.......' for _,g in grp): continue
        print('   '.join(g[r].ljust(25) for _,g in grp))
    print()
