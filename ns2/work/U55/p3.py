def run0(b):
    h = b.heights[0]
    k = 0
    r = h - 1
    while r >= 0 and b.grid[r][0] == 1:
        k += 1
        r -= 1
    if h + (4 - k) > 6:
        return 0
    return k

def fires(b):
    return run0(b) >= 2 and not poisoned(b)

def level(b):
    k = run0(b)
    if poisoned(b) and k < 3:
        return 1
    return {0: 0, 1: 1, 2: 5, 3: 9}.get(k, 9)

def poisoned(b):
    h = b.heights[0]
    return any((r, 0) in b.their_wins for r in range(h + 1, 6))
