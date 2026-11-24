def score_(b):
    M = [0] * 7
    T = [0] * 7
    for r in range(6):
        for c in range(7):
            v = b.grid[r][c]
            if v == 1:
                M[c] += 1
            elif v == 2:
                T[c] += 1
    s = 0.0
    if b.last_col == 1 or b.last_col == 6:
        s += 2
    s += T[1] + T[6] + 0.5 * T[4] + 0.5 * M[4]
    s -= 1.5 * T[0] + T[2] + 0.5 * M[2] + 0.5 * M[0]
    return s

def fires(b):
    return score_(b) >= 4.5

def level(b):
    return max(0, min(9, int(score_(b) + 1)))
