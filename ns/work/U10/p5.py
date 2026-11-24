def own(b, c):
    m = 0
    t = 0
    for r in range(6):
        v = b.grid[r][c]
        if v == 1:
            m += 1
        elif v == 2:
            t += 1
    return m, t

def well(b):
    h = b.heights
    if h[2] > 1 or h[3] < 4 or h[1] < 2:
        return -99
    m3, t3 = own(b, 3)
    m0, t0 = own(b, 0)
    s = h[1] + h[3] + h[0] // 2 - 3 * h[2] - (h[4] + h[5] + h[6]) // 2
    s += 2 * (m3 - t3) + (t0 - m0)
    return s

def fires(b):
    if b.ply == 1 and b.last_col == 0:
        return True
    return well(b) >= 9

def level(b):
    if b.ply == 1 and b.last_col == 0:
        return 3
    s = well(b)
    if s < 5:
        return 0
    return min(9, s - 4)
