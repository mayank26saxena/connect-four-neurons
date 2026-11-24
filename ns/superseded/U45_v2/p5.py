def own(b, r, c, wmine, wtheirs):
    v = b.grid[r][c]
    if v == 1:
        return wmine
    if v == 2:
        return wtheirs
    return 0

def score(b):
    h = b.heights
    s = 0.0
    if h[2] == 0:
        s += 3
    elif h[2] == 5:
        s += 2
    if b.ply < 6 or b.ply > 22:
        s -= 3
    elif b.ply > 16:
        s -= 1
    rough = sum(abs(h[c] - h[c + 1]) for c in range(6))
    s += 0.4 * (rough - (0.6 * b.ply + 3.5))
    s += own(b, 0, 3, 1, -1)
    s += own(b, 1, 3, -0.5, 0.5)
    s += own(b, 2, 3, 0.5, -0.5)
    s += own(b, 1, 4, 0.5, -1)
    s += own(b, 2, 4, 0.5, -1.5)
    for r in range(3):
        s += own(b, r, 0, -0.3, 0.3)
    s += own(b, 0, 1, -0.5, 0.3)
    return s

def fires(b):
    s = score(b)
    return max(0.0, min(1.0, (s - 2.0) / 3.0))

def level(b):
    return int(max(0, min(9, round((score(b) - 1.0) * 2))))
