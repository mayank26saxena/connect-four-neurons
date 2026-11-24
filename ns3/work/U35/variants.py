import sys
sys.path.insert(0,'.')
from c4n import ns
mv=[int(x) for x in sys.argv[1].split(',')]
K=int(sys.argv[2])
n=len(mv)
seen=set()
def ok(s):
    try:
        for t in range(4,len(s)+1):
            b=ns.board_from_moves(s[:t])
        # no completed four: check that each move was not a win cell for mover
        for t in range(len(s)):
            b=ns.board_from_moves(s[:t])
            r=b.landing(s[t])
            if r is None or (r,s[t]) in b.my_wins: return False
        return True
    except Exception:
        return False
for i in range(n-K,n):
    for j in range(i+2,n,2):
        s=mv[:]; s[i],s[j]=s[j],s[i]
        if tuple(s) in seen or s==mv: continue
        seen.add(tuple(s))
        if ok(s): print(','.join(map(str,s)))
