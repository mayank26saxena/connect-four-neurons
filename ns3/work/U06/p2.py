def vthree(b, c):
    # opponent has three stacked on top of column c with the cell above empty
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    c = b.last_col
    if c is None or len(b.my_playable_wins) > 0:
        return False
    return vthree(b, c)

def level(b):
    if not fires(b):
        return 1
    return 9 if b.last_col == 5 else 6
