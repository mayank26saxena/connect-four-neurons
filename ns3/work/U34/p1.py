def vthree(b, c):
    # opponent has three stacked on top of column c with the cell above empty
    h = b.heights[c]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return vthree(b, 5)

def level(b):
    if vthree(b, 5):
        return 9 if b.last_col == 5 else 7
    if any(vthree(b, c) for c in range(7)):
        return 3
    return 0
