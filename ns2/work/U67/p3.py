def since_fill(b):
    # moves played since the stone that filled column 1 (None if column 1 not full)
    if b.heights[1] != 6:
        return None
    m = b.moves
    for i in range(len(m) - 1, -1, -1):
        if m[i] == 1:
            return len(m) - 1 - i
    return None

def level(b):
    s = since_fill(b)
    if s == 0:
        if b.ply >= 18:
            return 9
        if b.ply >= 12:
            return 7
        return 5
    if s is not None:
        if b.ply >= 26 and s <= 8:
            return 6
        if b.ply >= 26:
            return 5
        if b.ply >= 18:
            return 4
        return 2
    if b.last_col == 1 and b.last_row == 4:
        return 3
    return 0

def fires(b):
    return level(b) >= 6
