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
        if p >= 40:
            return 7
        if p >= 37:
            return 6
        if p >= 32:
            return 5
        if p >= 26:
            return 4
        return 2
    if b.last_col == 1 and b.last_row == 4:
        return 3
    return 0

def fires(b):
    return level(b) >= 6
