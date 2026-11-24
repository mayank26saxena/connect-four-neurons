def fires(b):
    c = b.last_col
    if c is None or b.last_row != 2:
        return False
    return max(b.heights) <= 3

def level(b):
    c = b.last_col
    if c is None:
        return 0
    if b.last_row == 2:
        s = 3
        if max(b.heights) <= 3:
            s = 6
            if 2 <= c <= 5:
                s += 1
            if b.grid[1][c] == 1:
                s += 1
            if b.ply <= 8:
                s += 1
        return s
    if max(b.heights) <= 2 and b.ply <= 8:
        return 2
    return 0
