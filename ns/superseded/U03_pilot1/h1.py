from lab import *
def h_rowtwo(b):
    # some horizontal 4-window with >=2 mine, 0 theirs
    for r in range(6):
        for c0 in range(4):
            w=[b.grid[r][c0+k] for k in range(4)]
            if 2 not in w and w.count(1)>=2: return True
    return False
evaluate(h_rowtwo, show=0)
def h_bottom(b):
    r=0
    for c0 in range(4):
        w=[b.grid[r][c0+k] for k in range(4)]
        if 2 not in w and w.count(1)>=2: return True
    return False
evaluate(h_bottom)
