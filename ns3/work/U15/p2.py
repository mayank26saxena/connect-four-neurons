def vthree(b, c):
    # opponent has three stacked on top of column c and the cell above is empty
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    if len(b.legal) < 2:
        return False
    return any(vthree(b, c) for c in range(7))

def level(b):
    if len(b.legal) < 2:
        return 0
    if vthree(b, 6):
        return 8 if b.last_col == 6 else 6
    if vthree(b, 0):
        return 6 if b.last_col == 0 else 5
    for c in range(1, 6):
        if vthree(b, c):
            return 5
    return 0
