# opening with centre column (nearly) empty, scored by who holds which bottom-row cells
W_ME = [-1.0, 1.5, 0.3, 0.0, -0.5, 1.5, -1.0]
W_TH = [0.0, -1.0, 0.0, 0.0, 0.3, -1.0, 1.5]

def score(b):
    if b.ply < 3 or b.ply > 16 or b.heights[3] > 1:
        return -9.0
    g = b.grid
    row = g[0]
    s = 2.0 if b.heights[3] == 0 else 1.0
    for c in range(7):
        if c == 3:
            continue
        if row[c] == 1:
            s += W_ME[c]
        elif row[c] == 2:
            s += W_TH[c]
    if row[1] == 1 and row[2] == 1:
        s += 1.5
    if row[5] == 1 and row[4] == 1:
        s += 1.0
    if row[5] == 1 and g[1][5] == 2:
        s += 1.0
    if row[1] == 1 and g[1][1] == 2:
        s += 0.5
    return s

def fires(b):
    return score(b) >= 4.0

def level(b):
    s = score(b)
    if s < 2.0:
        return 0
    return max(0, min(9, int(round((s - 2.0) * 2))))
