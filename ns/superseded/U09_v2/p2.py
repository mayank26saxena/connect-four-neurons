HOT = [(3, 0), (3, 1), (3, 2), (4, 0), (2, 3)]

def fires(b):
    return any(cell in b.their_wins for cell in HOT)

def level(b):
    n = sum(1 for cell in HOT if cell in b.their_wins)
    g = b.grid
    o = sum(1 for (r, c) in [(2, 2), (1, 3), (2, 1), (1, 2)] if g[r][c] == 2)
    if n == 0:
        return min(3, o // 2)
    return min(9, 4 + 2 * n + o // 2)
