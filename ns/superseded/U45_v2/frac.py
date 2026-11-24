import sys,re
for fn in sys.argv[1:]:
    ms=[]
    for l in open(fn):
        if l.startswith('[pos'):
            mv=re.search(r'moves:(.*?)last move',l).group(1).strip(); ms.append([int(x) for x in mv.split(',')] if mv else [])
    n=len(ms)
    print(fn,n,'col2 empty',sum(2 not in m for m in ms)/n,'any empty col',sum(any(c not in m for c in range(7)) for m in ms)/n,
      'col1 empty',sum(1 not in m for m in ms)/n,'ply<=20',sum(len(m)<=20 for m in ms)/n,
      'col2 empty or h2==5',sum(m.count(2) in (0,5) for m in ms)/n)
