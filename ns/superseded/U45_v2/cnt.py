import sys,re,collections
def parse(fn):
    L=open(fn).read().split('\n'); out={}
    for l in L:
        if l.startswith('[pos'):
            pid=int(re.search(r'pos (\d+)',l).group(1))
            mv=re.search(r'moves:(.*?)last move',l).group(1).strip()
            out[pid]=[int(x) for x in mv.split(',')] if mv else []
    return list(out.values())
for fn in sys.argv[1:]:
    d=[m for m in parse(fn) if 6<=len(m)<=20 and 2 not in m]
    print(fn,len(d),'h3',sorted(collections.Counter(m.count(3) for m in d).items()),'h1',sorted(collections.Counter(m.count(1) for m in d).items()),'ply',sorted(collections.Counter(len(m) for m in d).items()))
