def win_free(b, cells):
    v = [b.grid[r][c] for r, c in cells]
    if 1 in v:
        return 0
    return v.count(2)

def fires(b):
    return win_free(b, [(0, 3), (0, 4), (0, 5), (0, 6)]) >= 2

def level(b):
    k = win_free(b, [(0, 3), (0, 4), (0, 5), (0, 6)])
    return [0, 2, 6, 8, 9][k]
