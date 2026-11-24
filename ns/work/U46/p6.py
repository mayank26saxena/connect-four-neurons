# their stones outside column 2 subtract; my stones mostly neutral; diluted by total stones
KT = [0.6, 0.4, 0.0, 0.6, 0.25, 0.2, 0.15]
KM = [0.1, 0.0, 0.0, 0.05, -0.3, 0.3, 0.0]

def score(b):
    s = float(b.heights[2])
    for c in range(7):
        if c == 2:
            continue
        for r in range(6):
            v = b.grid[r][c]
            if v == 2:
                s -= KT[c]
            elif v == 1:
                s -= KM[c]
    if b.last_col == 5:
        s += 0.7
    return s

def ratio(b):
    return score(b) / (b.ply + 4)

def fires(b):
    if b.ply == 1:
        return b.heights[2] == 1
    return b.heights[2] >= 3 and ratio(b) >= 0.3

def level(b):
    if b.ply == 1:
        return 3 if b.heights[2] == 1 else 0
    if b.heights[2] < 2:
        return 0
    x = ratio(b) * score(b)
    return max(0, min(9, int((x - 0.6) * 4)))
