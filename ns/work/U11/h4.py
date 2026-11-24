def opp_run_top(b, c):
    h = b.heights[c]
    n = 0
    while n < h and b.grid[h - 1 - n][c] == 2:
        n += 1
    return n

def fires(b):
    if b.heights[6] >= 6:
        return False
    return opp_run_top(b, 6) >= 2

def level(b):
    if b.heights[6] >= 6:
        return 0
    n = opp_run_top(b, 6)
    if n >= 3:
        return {3: 9, 4: 7, 5: 4}[b.heights[6]]
    if n == 2:
        return 2
    return 0
