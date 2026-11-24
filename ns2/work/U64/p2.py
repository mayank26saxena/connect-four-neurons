def fires(b):
    h0 = b.heights[0]
    if h0 < 1 or h0 > 2:
        return False
    second = 2 if b.me_first else 1
    return all(b.grid[r][0] == second for r in range(h0))

def level(b):
    if not fires(b):
        return 0
    return 5
