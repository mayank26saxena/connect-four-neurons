def top_run(b, who):
    h = b.heights[0]
    n = 0
    while n < h and b.grid[h - 1 - n][0] == who:
        n += 1
    return n

def fires(b):
    if b.heights[0] >= 6:
        return False
    return top_run(b, 2) >= 2

def level(b):
    if b.heights[0] >= 6:
        return 0
    t = top_run(b, 2)
    if t >= 3:
        return 9
    if t == 2:
        return 2
    if top_run(b, 1) >= 3:
        return 1
    return 0
