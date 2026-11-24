def score(b):
    if b.heights[1] != 1:
        return -100
    h = b.heights
    full = sum(1 for c in range(7) if h[c] == 6)
    s = b.ply + h[3] + 0.5 * (h[0] + h[2]) + 2 * full
    if b.last_col == 1:
        s += 6
    return s

def fires(b):
    return score(b) >= 23

def level(b):
    s = score(b)
    if s < 0:
        return 0
    return int(max(1, min(9, (s - 11) / 3)))
