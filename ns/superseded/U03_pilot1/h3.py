from lab import *
from h2 import hist
def run(b, r, c, p, dr, dc):
    n=0; rr,cc=r+dr,c+dc
    while 0<=rr<6 and 0<=cc<7 and b.grid[rr][cc]==p: n+=1; rr+=dr; cc+=dc
    return n
def hrun(b,c,p=1):
    r=b.landing(c)
    if r is None: return -1
    return run(b,r,c,p,0,1)+run(b,r,c,p,0,-1)
for c in range(7):
    print('hrun me col',c); hist(lambda b: hrun(b,c))
