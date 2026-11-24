LAST = [2.0, 3.0, 1.5, -1.0, -1.0, -1.0, 1.5]
THEIRV = [1.0, 1.0, 1.0, -0.5, -1.5, -0.5, 0.3]

def score(b):
    c = b.last_col
    if c is None:
        return -9
    s = LAST[c]
    tv = []
    mine1 = 0
    for r in range(6):
        for col in range(7):
            if b.grid[r][col] == 2:
                tv.append(THEIRV[col])
            elif b.grid[r][col] == 1 and col == 1:
                mine1 += 1
    if tv:
        s += 2.0 * sum(tv) / len(tv)
    s -= 1.0 * mine1
    if 20 <= b.ply < 30:
        s -= 2.0
    return s

def fires(b):
    return score(b) >= 3.2

def level(b):
    s = score(b)
    if s < 2.0:
        return 0
    return max(0, min(9, int(round((s - 2.0) * 3))))
