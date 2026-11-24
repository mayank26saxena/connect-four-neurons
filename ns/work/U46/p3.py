def cnt(b, c, who):
    return sum(1 for r in range(6) if b.grid[r][c] == who)

def fires(b):
    if b.ply == 1:
        return b.heights[2] == 1
    return cnt(b, 2, 2) >= 3

def level(b):
    if b.ply == 1:
        return 3 if b.heights[2] == 1 else 0
    t = cnt(b, 2, 2)
    m = cnt(b, 2, 1)
    s = t + 0.5 * m - 0.1 * b.ply
    return max(0, min(9, int(s * 1.5)))
