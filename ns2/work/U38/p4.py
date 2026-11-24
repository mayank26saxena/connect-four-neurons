def run0(b):
    r = b.heights[0] - 1
    n = 0
    while r >= 0 and b.grid[r][0] == 2:
        n += 1
        r -= 1
    return n

def pair23(b):
    return b.heights[0] == 4 and b.grid[2][0] != 0 and b.grid[2][0] == b.grid[3][0]

def fires(b):
    if b.landing(0) is None:
        return False
    return run0(b) >= 3 or pair23(b)

def level(b):
    if b.landing(0) is None:
        return 0
    n = run0(b)
    if n >= 3:
        return 9 if b.heights[0] >= 4 else 8
    if pair23(b):
        return 3 if b.grid[3][0] == 2 else 2
    return 0
