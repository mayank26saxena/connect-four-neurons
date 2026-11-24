def vthree(b, c):
    # opponent has three stacked on top of column c with the cell above empty
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return b.last_col == 5 and vthree(b, 5)

def level(b):
    if fires(b):
        return 9
    if b.last_col is not None and vthree(b, b.last_col):
        return 2
    return 0
