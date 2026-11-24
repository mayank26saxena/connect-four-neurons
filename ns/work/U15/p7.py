def col3(b):
    t = 0
    m = 0
    for r in range(b.heights[3]):
        if b.grid[r][3] == 2:
            t += 1
        else:
            m += 1
    return m, t

def raw(b):
    g = b.grid
    m, t = col3(b)
    if t > 0:
        return 0
    s = 2.0
    if g[0][0] == 2:
        s += 3
    if g[0][6] == 2:
        s += 2
    if g[0][1] == 2:
        s += 1
    if m >= 1:
        s += 1
    if b.me_first:
        s += 1
    return s

def fires(b):
    return raw(b) >= 6

def level(b):
    return max(0, min(9, int(raw(b))))
