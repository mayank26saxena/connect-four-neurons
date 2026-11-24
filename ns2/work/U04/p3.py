def score_(b):
    s = 0
    if b.ply <= 6:
        s += 3
    elif b.ply <= 10:
        s += 1
    s += sum(1 for c in (1, 2, 4) if b.heights[c] == 0)
    c = b.last_col
    if c is not None:
        r = b.last_row
        left = b.grid[r][c-1] if c > 0 else 0
        right = b.grid[r][c+1] if c < 6 else 0
        if left == 0 and right == 0:
            s += 1
    return s

def fires(b):
    return score_(b) >= 5

def level(b):
    return min(9, score_(b) + 2)
