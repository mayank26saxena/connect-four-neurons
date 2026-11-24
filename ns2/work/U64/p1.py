def fires(b):
    h0 = b.heights[0]
    if h0 < 1 or h0 > 2:
        return False
    if b.grid[0][0] != 1:
        return False
    return (not b.me_first) and b.ply >= 11

def level(b):
    if not fires(b):
        return 0
    return 6 if 13 <= b.ply <= 21 else 3
