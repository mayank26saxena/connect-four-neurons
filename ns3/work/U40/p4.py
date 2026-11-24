def _best(b):
    g = b.grid
    best = 0
    for (r, c) in [(0, 2), (0, 3), (1, 2), (1, 3)]:
        if g[r][c] != 1:
            continue
        n = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < 6 and 0 <= cc < 7 and g[rr][cc] == 2:
                    n += 1
        best = max(best, n)
    return best

def fires(b):
    if b.ply > 16 or b.heights[4] > 1:
        return False
    return _best(b) >= 3

def level(b):
    if b.ply > 16:
        return 0
    n = _best(b)
    if b.heights[4] > 1:
        n -= 1
    return max(0, min(9, [0, 0, 1, 4, 7, 9, 9, 9, 9][max(n, 0)]))
