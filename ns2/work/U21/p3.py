def _k(b):
    s = 0
    for c in (3, 4):
        for r in range(b.heights[c]):
            v = b.grid[r][c]
            want = 1 if (r + c) % 2 == 1 else 2
            s += 1 if v == want else -1
    return s

def fires(b):
    return _k(b) >= 3

def level(b):
    return max(0, min(9, 2 * _k(b) - 1))
