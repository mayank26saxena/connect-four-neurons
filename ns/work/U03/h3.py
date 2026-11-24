# bottom-row configuration score in the opening, centre column still (nearly) empty
W_ME = [-1.0, 1.5, 0.3, 0.0, -0.5, 1.5, -1.0]
W_TH = [0.0, -1.0, 0.0, 0.0, 0.3, -1.0, 1.5]

def score(b):
    if b.ply < 3 or b.ply > 16 or b.heights[3] > 1:
        return -9.0
    s = 2.0 if b.heights[3] == 0 else 1.0
    row = b.grid[0]
    for c in range(7):
        if c == 3:
            continue
        if row[c] == 1:
            s += W_ME[c]
        elif row[c] == 2:
            s += W_TH[c]
    return s

def fires(b):
    return score(b) >= 3.5

def level(b):
    s = score(b)
    if s < 2.0:
        return 0
    return max(0, min(9, int(round((s - 2.0) * 2.5))))
