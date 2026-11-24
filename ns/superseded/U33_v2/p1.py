def run6(b):
    # length of the opponent's run at the top of column 6
    h = b.heights[6]
    n = 0
    r = h - 1
    while r >= 0 and b.grid[r][6] == 2:
        n += 1
        r -= 1
    return n

def fires(b):
    return run6(b) >= 2 and b.heights[6] < 6

def level(b):
    n = run6(b)
    if b.heights[6] >= 6:
        return 0
    return [0, 1, 6, 9][min(n, 3)]
