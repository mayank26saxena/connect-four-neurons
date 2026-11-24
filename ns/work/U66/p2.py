def pts(b):
    h = b.heights
    s = 0
    if h[1] == 0: s += 1
    if h[5] == 0: s += 1
    if h[4] == 2: s += 2
    elif 1 <= h[4] <= 4: s += 1
    else: s -= 2
    o_even = sum(1 for r in range(6) for c in (0, 2, 6) if b.grid[r][c] == 2)
    o_odd = sum(1 for r in range(6) for c in (1, 5) if b.grid[r][c] == 2)
    s += min(o_even, 4) * 0.5 - o_odd * 0.5
    if b.last_col in (0, 2, 6): s += 1
    return s

def fires(b):
    return pts(b) >= 5

def level(b):
    return max(0, min(9, int(round((pts(b) - 2) * 1.5))))
