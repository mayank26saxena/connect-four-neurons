def nth(b, c):
    return sum(1 for r in range(6) if b.grid[r][c] == 2)

def recent4(b):
    m = b.moves
    return (len(m) >= 1 and m[-1] == 4) or (len(m) >= 3 and m[-3] == 4)

def fires(b):
    return nth(b, 4) >= 2 and b.heights[5] <= 1 and recent4(b) and b.ply <= 24

def level(b):
    n = nth(b, 4)
    s = 0
    if n >= 2:
        s = 3 + min(n, 4)
        if recent4(b):
            s += 2
        s -= 2 * b.heights[5]
        s -= max(0, b.ply - 14) // 4
    elif n == 1 and recent4(b):
        s = 2
    return max(0, min(9, s))
