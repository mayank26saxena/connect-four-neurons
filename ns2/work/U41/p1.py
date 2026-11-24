D = [(0, 0), (1, 1), (2, 2), (3, 3)]

def cnt(b):
    th = sum(1 for (r, c) in D if b.grid[r][c] == 2)
    mine = sum(1 for (r, c) in D if b.grid[r][c] == 1)
    return th, mine

def fires(b):
    th, mine = cnt(b)
    return mine == 0 and th >= 2

def level(b):
    th, mine = cnt(b)
    if mine > 0 or th < 2:
        return 0
    return 4 if th == 2 else 9
