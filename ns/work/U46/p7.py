# column-2 stones (either colour) push it up; opponent stones elsewhere (esp. cols 0, 1, 3) push it down;
# my stones elsewhere are nearly neutral (my col-4 stones help, my col-5 stones hurt); mild dilution with ply.
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
    return s - 0.04 * b.ply

def fires(b):
    if b.ply == 1:
        return b.heights[2] == 1
    return score(b) >= 3.0

def level(b):
    if b.ply == 1:
        return 3 if b.heights[2] == 1 else 0
    return max(0, min(9, int((score(b) - 2.0) * 2)))
