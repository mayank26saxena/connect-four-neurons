LAST = [2.2, 3.0, 1.6, 0.0, 0.0, 0.0, 1.4]

def frac(b, who):
    cnt = [0] * 7
    tot = 0
    for r in range(6):
        for c in range(7):
            if b.grid[r][c] == who:
                cnt[c] += 1
                tot += 1
    return [x / max(1, tot) for x in cnt]

def score(b):
    c = b.last_col
    if c is None or b.ply >= 20:
        return -9
    m = frac(b, 1)
    t = frac(b, 2)
    s = LAST[c]
    s -= 3.0 * m[4] + 3.0 * m[1] + 1.0 * (m[3] + m[5])
    s -= 1.0 * t[4]
    s += 0.5 * (t[0] + t[1] + t[2])
    if c == 1 and b.heights[1] > 2:
        s -= 1.0
    if b.ply >= 16:
        s -= 0.5
    return s

def fires(b):
    c = b.last_col
    if c is None or b.ply >= 20:
        return False
    m = frac(b, 1)
    if m[1] > 0 or m[4] >= 0.5:
        return False
    if c == 1:
        return b.heights[1] <= 2
    if c == 0:
        return b.heights[0] == 1 and b.ply <= 10
    if c == 2:
        return b.heights[2] == 1 and b.ply <= 8
    return False

def level(b):
    s = score(b)
    if s < 0.5:
        return 0
    v = int(round((s - 0.5) * 3))
    if fires(b):
        v = max(v, 5)
    else:
        v = min(v, 4)
    return max(0, min(9, v))
