def nth(b, c):
    return sum(1 for r in range(6) if b.grid[r][c] == 2)

def fires(b):
    return nth(b, 4) >= 2 and b.heights[5] == 0

def level(b):
    n = nth(b, 4)
    if b.heights[5] > 1:
        return 0
    s = n * 2 - b.heights[5] * 2
    return max(0, min(9, s))
