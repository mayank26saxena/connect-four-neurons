import sys,re,collections
for fn in sys.argv[1:]:
    ms=[]
    for l in open(fn):
        if l.startswith('[pos'):
            mv=re.search(r'moves:(.*?)last move',l).group(1).strip(); ms.append([int(x) for x in mv.split(',')] if mv else [])
    print(fn,[sorted(collections.Counter(m.count(c) for m in ms).items()) for c in (1,2,3)])
