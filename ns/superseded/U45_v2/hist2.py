import sys,re
def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for l in L:
        if l.startswith('[pos'):
            mv=re.search(r'moves:(.*?)last move',l).group(1).strip()
            out.append([int(x) for x in mv.split(',')] if mv else [])
    return out
for fn in sys.argv[1:]:
    d=[m for m in parse(fn) if 6<=len(m)<=20 and 2 not in m]
    n=len(d); S=[0]*7; H=[0]*7
    for mv in d:
        me=len(mv)%2  # index parity of my moves
        for i,c in enumerate(mv):
            S[c]+= 1 if i%2==me else -1
            H[c]+=1
    print(fn,n,'mine-theirs per col',[round(s/n,2) for s in S],'height',[round(h/n,2) for h in H])
