def fires(b):
    if b.ply > 12 or max(b.heights) > 4:
        return False
    if len(b.my_wins) > 0:
        return False
    # weak col-3 hint: their stone directly on my centre stone
    return b.heights[3] in (2, 4) and b.grid[1][3] == 2

def level(b):
    s = 0
    if max(b.heights) <= 4 and b.ply <= 12 and len(b.my_wins) == 0:
        s = 3
        if b.heights[3] in (2, 4) and b.grid[1][3] == 2:
            s = 7
    return s
