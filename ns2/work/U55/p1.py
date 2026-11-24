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
    return run0(b) >= 2

def level(b):
    k = run0(b)
    return {0: 0, 1: 1, 2: 5, 3: 9}.get(k, 9)
