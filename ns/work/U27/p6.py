def s(b):
    h0 = b.heights[0]
    if h0 < 4:
        return -9.0
    mine = sum(1 for r in range(h0) if b.grid[r][0] == 1)
    v = (h0 - 4) + 0.7 * (mine - h0 / 2.0)
    if b.last_col == 0:
        v = v + 0.6
    v = v - 0.25 * b.heights[1] - 0.03 * b.ply - 0.12 * max(0, b.ply - 26)
    return v

def fires(b):
    return s(b) >= 0.45

def level(b):
    v = s(b)
    if v <= 0:
        return 0
    return max(1, min(9, int(round(v * 3))))
