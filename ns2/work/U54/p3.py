def towers(b):
    h = b.heights
    n = 0
    for c in range(7):
        if h[c] == 0 or b.grid[h[c] - 1][c] != 2:
            continue
        for d in (c - 1, c + 1):
            if 2 <= d <= 4 and h[c] >= h[d] + 2:
                n += 1
    return n

def fires(b):
    return towers(b) >= 2

def level(b):
    return min(9, 3 * towers(b))
