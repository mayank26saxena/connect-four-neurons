from lab import *
from h2 import hist
def col3thr(b, which='any', only_unplay=True):
    L=b.landing(3)
    if L is None: return False
    S = b.my_wins|b.their_wins if which=='any' else (b.my_wins if which=='me' else b.their_wins)
    return any(c==3 and (r>L or not only_unplay) for r,c in S)
print('any unplay'); evaluate(col3thr)
print('any incl play'); evaluate(lambda b: col3thr(b,'any',False))
print('me'); evaluate(lambda b: col3thr(b,'me'))
print('them'); evaluate(lambda b: col3thr(b,'them'))
print('col3thr or early h3==0'); evaluate(lambda b: col3thr(b) or (3<=b.ply<=10 and b.heights[3]==0))
for c in range(7):
    print('col',c, end=' '); evaluate(lambda b: any(cc==c and r>(b.landing(c) if b.landing(c) is not None else 9) for r,cc in b.my_wins|b.their_wins))
print('n threat cells in col 3'); hist(lambda b: sum(1 for r,c in b.my_wins|b.their_wins if c==3))
