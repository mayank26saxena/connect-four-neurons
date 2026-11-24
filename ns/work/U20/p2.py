def blocked(b):
    if b.last_col is None:
        return 0
    r, c = b.last_row, b.last_col
    best = 0
    for s in range(max(0, c - 3), min(3, c) + 1):
        cells = [b.grid[r][s + k] for k in range(4) if s + k != c]
        if 2 in cells:
            continue
        best = max(best, cells.count(1))
    return best

def fires(b):
    return blocked(b) >= 2

def level(b):
    k = blocked(b)
    return 0 if k < 2 else (5 if k == 2 else 8)
