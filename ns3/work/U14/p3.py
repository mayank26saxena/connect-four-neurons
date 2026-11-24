def vert1(b):
    h = b.heights[1]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][1] == 2 for k in range(3))

def above_threat(b):
    c = b.last_col
    if c is None or b.last_row is None or b.last_row >= 5:
        return False
    return (b.last_row + 1, c) in b.their_wins

def fires(b):
    return vert1(b) or (b.last_col == 1 and above_threat(b))

def level(b):
    if vert1(b):
        return 9
    if b.last_col == 1 and above_threat(b):
        return 4
    return 0
