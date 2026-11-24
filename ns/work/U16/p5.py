def est(b):
    # opponent just dropped a stone in column 0 that landed on row 3 or 4 (4th/5th stone);
    # tall columns 1 and 2 weaken the response
    if b.last_col != 0 or b.last_row not in (3, 4):
        return 0.0
    base = 4.2 if b.last_row == 4 else 2.8 - 0.04 * max(0, b.ply - 10)
    h1, h2 = b.heights[1], b.heights[2]
    return base - 0.25 * max(h1, h2) - 0.1 * min(h1, h2)

def fires(b):
    return est(b) > 0.75

def level(b):
    if b.last_col != 0:
        return 0
    if b.last_row == 5:
        return 2
    e = est(b)
    if e <= 0:
        return 1 if b.last_row in (3, 4) else 0
    return max(3, min(9, int(e * 2.5)))
