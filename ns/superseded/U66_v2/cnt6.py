import sys,re,collections
for f in sys.argv[1:]:
    L=open(f).read().split('\n')
    c=collections.Counter(); n=0
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            m=re.search(r'moves: ([0-9,]*)',l).group(1)
            mv=[int(x) for x in m.split(',')] if m else []
            if len(mv)<2: continue
            n+=1; c['p%d'%mv[-2]]+=1
            c['pair%d%d'%(mv[-2],mv[-1])]+=0
    print(f.split('_')[-1],n,' '.join('%s:%.2f'%(k,c[k]/n) for k in sorted(c) if k[0]=='p' and len(k)==2))
