def level(b):
    full1 = b.heights[1] == 6
    fill = b.last_col == 1 and b.last_row == 5
    p = b.ply
    if fill:
        if p >= 26:
            return 9
        if p >= 18:
            return 8
        if p >= 12:
            return 6
        return 4
    if full1:
        q = p
        if b.grid[5][1] == 2:
            q += 4
        if b.last_col in (0, 2, 6):
            q += 4
        if q >= 46:
            return 7
        if q >= 42:
            return 6
        if q >= 36:
            return 5
        if q >= 28:
            return 4
        return 2
    if b.last_col == 1 and b.last_row == 4:
        return 3
    return 0

def fires(b):
    return level(b) >= 6
