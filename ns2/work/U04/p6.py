W = [2, 0, -1, 1, 1, 1, 2]

def total(b):
    s = 0
    if b.ply <= 6:
        s += 3
    elif b.ply <= 10:
        s += 1
    else:
        return 0
    s += sum(1 for c in (1, 2, 4) if b.heights[c] == 0)
    for c in range(7):
        if b.heights[c] == 2 and b.grid[0][c] == 1 and b.grid[1][c] == 2:
            s += W[c]
    return s

def fires(b):
    return total(b) >= 6

def level(b):
    s = total(b)
    return 9 if s >= 8 else (7 if s >= 7 else (5 if s >= 6 else 0))
