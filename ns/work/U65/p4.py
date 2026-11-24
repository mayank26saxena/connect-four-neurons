def top_run(b, c):
    h = b.heights[c]
    if h == 0 or h >= 6:
        return 0
    n = 0
    r = h - 1
    while r >= 0 and b.grid[r][c] == 2:
        n += 1
        r -= 1
    return n

def early(b):
    # opening: opponent has a bottom stone in col 3 or 5, I have no stone in cols 2-4
    if b.ply < 2 or b.ply > 6:
        return False
    if any(b.grid[r][c] == 1 for c in (2, 3, 4) for r in range(2)):
        return False
    return b.grid[0][3] == 2 or b.grid[0][5] == 2

def fires(b):
    if early(b):
        return True
    if b.heights[1] > 1:
        return False
    return any(top_run(b, c) >= 2 for c in range(2, 7))

def level(b):
    if not fires(b):
        return 0
    best = max(top_run(b, c) for c in range(7))
    if early(b):
        return 7
    return min(9, 3 + 2 * best)
