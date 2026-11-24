def vert5(b):
    h = b.heights[5]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][5] == 2 for k in range(3))

def center_left_full(b):
    if b.heights[2] < 6 or b.heights[3] < 6:
        return False
    others = sum(1 for c in (0, 1, 4, 5, 6) if b.heights[c] == 6)
    return others <= 1

def fires(b):
    return vert5(b) or center_left_full(b)

def level(b):
    if vert5(b):
        return 8 if b.last_col == 5 else 5
    if center_left_full(b):
        return 4
    return 0
