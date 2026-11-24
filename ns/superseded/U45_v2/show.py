import sys,re
L=open(sys.argv[1]).read().split('\n')
for i,l in enumerate(L):
    if l.startswith('[pos'):
        mv=re.search(r'moves:(.*?)last move',l).group(1).strip()
        mv=[int(x) for x in mv.split(',')] if mv else []
        if mv.count(2)>0:
            print(l[:60]); print('\n'.join(L[i+1:i+7]))
