def pairs23(b):
    # rows where columns 2 and 3 hold a same-colour horizontal pair and columns 1 and 4 are empty in that row
    g = b.grid
    n = 0
    for r in range(6):
        if g[r][2] != 0 and g[r][2] == g[r][3] and g[r][1] == 0 and g[r][4] == 0:
            n += 1
    return n

def tower(b):
    h = b.heights
    return min(h[2], h[3]) - max(h[1], h[4])

def fires(b):
    return pairs23(b) >= 1 and tower(b) >= 2

def level(b):
    t = tower(b)
    p = pairs23(b)
    if t < 1:
        return 0
    return min(9, 2 * t + 2 * p)
