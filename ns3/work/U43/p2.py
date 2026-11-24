def top_run(b):
    h = b.heights[1]
    k = 0
    r = h - 1
    while r >= 0 and b.grid[r][1] == 2:
        k += 1
        r -= 1
    return h, k

def other_block(b):
    return any(c != 1 for (r, c) in b.their_playable_wins)

def fires(b):
    h, k = top_run(b)
    return h in (4, 5) and k >= 2 and not other_block(b)

def level(b):
    h, k = top_run(b)
    if other_block(b) or h == 6 or h < 3 or k == 0:
        return 0
    if not fires(b):
        return 2 if (k >= 1 and h >= 3) else 0
    if k >= 3 and h == 5:
        return 9
    if k >= 3:
        return 7
    return 5
