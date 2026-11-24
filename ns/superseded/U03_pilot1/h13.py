from lab import *
def botwin(b): return any(r==0 for r,c in b.my_playable_wins)
def makes3(b):
    g=b.grid[0]
    for c in range(7):
        if g[c]!=0: continue
        for c0 in range(max(0,c-3),min(3,c)+1):
            w=[g[x] if x!=c else 1 for x in range(c0,c0+4)]
            if 2 not in w and w.count(1)>=3: return True
    return False
evaluate(botwin); evaluate(makes3); evaluate(lambda b: b.ply<=12 and makes3(b))
evaluate(lambda b: b.ply<=12 and (makes3(b) or b.heights[3]==0))
