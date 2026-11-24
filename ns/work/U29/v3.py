def score_(b):
    if b.last_col != 3 or b.last_row < 1:
        return -1.0
    mine3 = sum(1 for r in range(b.last_row) if b.grid[r][3] == 1)
    theirs3 = b.last_row - mine3
    other = sum(b.heights) - b.heights[3]
    s = 0.1 * min(other, 14) - 1.06
    bonus = [0.0, 0.75, 1.15, 1.15, 0.95, 0.9][mine3]
    s += bonus + 0.05 * theirs3
    w = [0.05, 0.0, -0.05, 0.0, -0.12, -0.05, -0.035]
    s += sum(w[c] * b.heights[c] for c in range(7))
    return s

def fires(b):
    return score_(b) > 0.8

def level(b):
    s = score_(b)
    if s < 0:
        return 0
    return max(0, min(9, int(s * 5)))
