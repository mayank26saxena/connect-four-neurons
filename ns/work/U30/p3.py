def score(b):
    if b.heights[1] != 1:
        return -100
    full = sum(1 for c in range(7) if b.heights[c] == 6)
    s = b.ply + 2 * full
    if b.last_col == 1:
        s += 6
    return s

def fires(b):
    return score(b) >= 18

def level(b):
    s = score(b)
    if s < 0:
        return 0
    return max(1, min(9, (s - 6) // 3))
