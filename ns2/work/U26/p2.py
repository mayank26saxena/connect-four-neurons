def col2_top_odd_O(b):
    h = b.heights[2]
    return h in (1, 3) and b.grid[h - 1][2] == 2

def fires(b):
    return col2_top_odd_O(b) and b.ply <= 20

def level(b):
    if not col2_top_odd_O(b):
        return 0
    return 6 if b.ply <= 20 else 2
