def fires(b):
    return b.ply <= 14 and b.last_col == 2 and b.last_row is not None and b.last_row >= 1

def level(b):
    if b.last_col is None:
        return 0
    s = 0
    if b.ply <= 14:
        s += 3
    if b.last_col == 2:
        s += 3
    if b.last_row is not None and b.last_row >= 1:
        s += 2
    return min(9, s)
