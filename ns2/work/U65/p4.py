def _pairs(b):
    g = b.grid
    n = 0
    for r in range(4):
        for c in range(2, 6):
            if g[r][c] != 2:
                continue
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                rr, cc = r + dr, c + dc
                if 0 <= rr < 6 and 2 <= cc <= 5 and g[rr][cc] == 2:
                    n += 1
    return n

def fires(b):
    g = b.grid
    if b.ply > 14:
        return False
    if any(g[r][6] == 1 for r in range(6)):
        return False
    if g[0][2] == 1:
        return False
    return _pairs(b) >= 1

def level(b):
    if not fires(b):
        return 0
    return min(9, 3 + 2 * _pairs(b))
