HOT = {(2, 1): 3, (2, 2): 3, (3, 1): 2, (1, 3): 1, (2, 0): 1, (4, 0): 1, (1, 1): 1}

def nbrs(b, r, c):
    n = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr, cc = r + dr, c + dc
            if 0 <= rr < 6 and 0 <= cc < 7 and b.grid[rr][cc] == 2:
                n += 1
    return n

def score(b):
    if b.last_col is None:
        return 0
    cell = (b.last_row, b.last_col)
    w = HOT.get(cell, 0)
    if w == 0:
        return 0
    return w + nbrs(b, cell[0], cell[1])

def fires(b):
    return score(b) >= 5

def level(b):
    return min(9, max(0, 2 * (score(b) - 3)))
