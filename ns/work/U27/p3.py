def s(b):
    h0 = b.heights[0]
    if h0 < 4:
        return -9.0
    mine = sum(1 for r in range(h0) if b.grid[r][0] == 1)
    theirs = h0 - mine
    v = (h0 - 4) + (1.0 if b.last_col == 0 else 0.0) + 0.5 * (mine - theirs)
    v = v - 0.4 * b.heights[1] - 0.04 * b.ply
    return v

def fires(b):
    return s(b) >= 1.0

def level(b):
    v = s(b)
    if v < 0:
        return 0
    return max(0, min(9, int(round(v * 3))))
