def run2(b):
    # length of my own unbroken run on top of column 2 (0 if column full)
    h = b.heights[2]
    if h >= 6:
        return 0
    k = 0
    r = h - 1
    while r >= 0 and b.grid[r][2] == 1:
        k += 1
        r -= 1
    return k

def fires(b):
    return run2(b) >= 2

def level(b):
    k = run2(b)
    if k >= 3:
        return 9
    if k == 2:
        return 5
    return 0
