def fires(b):
    return b.last_col == 5 and b.ply >= 24 and b.heights[5] <= 4

def level(b):
    if b.last_col != 5:
        return 0
    s = 0
    if b.ply >= 20:
        s += 2
    if b.ply >= 28:
        s += 2
    if b.heights[5] <= 4:
        s += 2
    if b.heights[5] <= 3:
        s += 1
    full = sum(1 for c in range(7) if b.heights[c] == 6)
    s += min(2, full // 2)
    return min(9, s)
