def row0_open_three(b):
    g = b.grid[0]
    for s in range(1, 4):
        p = g[s]
        if p != 0 and g[s + 1] == p and g[s + 2] == p and g[s - 1] == 0 and s + 3 <= 6 and g[s + 3] == 0:
            return True
    return False

def full_cols(b):
    return sum(1 for c in range(7) if b.heights[c] == 6)

def fires(b):
    return row0_open_three(b) or full_cols(b) >= 5

def level(b):
    if row0_open_three(b):
        return 9
    f = full_cols(b)
    if f >= 5:
        return 5
    if f == 4:
        return 3
    return 0
