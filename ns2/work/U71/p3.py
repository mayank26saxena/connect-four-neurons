def run_from(b, c, r):
    k = 0
    while r >= 0 and b.grid[r][c] == 2:
        k += 1
        r -= 1
    return k, r + 1

def fires(b):
    return level(b) >= 4

def level(b):
    v = base(b)
    if b.my_playable_wins and v > 3:
        v = 3
    return v

def base(b):
    h = b.heights[3]
    if h == 0:
        return 0
    if h < 6:
        k, lo = run_from(b, 3, h - 1)
        if k >= 3 and lo >= 1:
            return 9
        if k >= 3:
            return 4
        if k == 2 and lo == 2:
            return 5
        if k == 2:
            return 2
        return 0
    # full column: opponent three just under my blocking stone
    if b.grid[5][3] == 1:
        k, lo = run_from(b, 3, 4)
        if k >= 3:
            return 4
    return 0
