# greedy hill climb for synthesis: add one stone of each colour per step, measured with the act tool
import subprocess, sys
sys.path.insert(0, 'ns/work/U58')
from mk import solve
def act(seq):
    o = subprocess.run(['uv','run','python','scripts/31_ns_tool.py','act','U58','--moves',seq],capture_output=True,text=True).stdout
    l = [x for x in o.split('\n') if 'after' in x][-1]
    return float(l.split(':')[1].split()[0])
def add(rows, c, ch):
    g=[list(r) for r in rows[::-1]]
    for r in range(6):
        if g[r][c]=='.': g[r][c]=ch; return [''.join(x) for x in g[::-1]]
    return None
rows=sys.argv[1].split('/'); steps=int(sys.argv[2])
best=act(solve(rows)); print(best, '/'.join(rows), flush=True)
for s in range(steps):
    cand=None
    for a in range(7):
        r1=add(rows,a,'X')
        if not r1: continue
        for bcol in range(7):
            r2=add(r1,bcol,'O')
            if not r2: continue
            seq=solve(r2)
            if not seq: continue
            v=act(seq)
            if cand is None or v>cand[0]: cand=(v,r2,seq)
    if cand is None or cand[0]<=best: break
    best,rows,seq=cand; print(best,'/'.join(rows),seq,flush=True)
