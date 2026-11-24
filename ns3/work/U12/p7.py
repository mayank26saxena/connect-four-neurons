def val(b):
    # last stone in column 0; taller column 0 raises it, longer game lowers it,
    # and it is damped when the mover's opponent (me) owns more of column 0 than the mover
    if b.last_col != 0:
        return -9.0
    h = b.heights[0]
    o = 0
    x = 0
    for r in range(h):
        if b.grid[r][0] == 2:
            o += 1
        else:
            x += 1
    v = h - b.ply / 6.0
    v = v - 0.9 * max(0, x - o)
    if x == 0:
        v = v - 2.0
    if h == 3:
        v = v - 1.5
    if h <= 2:
        v = v - 4.0
    return v

def fires(b):
    return val(b) >= 0.0

def level(b):
    v = val(b)
    if v < -3:
        return 0
    return max(1, min(9, int(round(1.5 * v + 3.2))))
