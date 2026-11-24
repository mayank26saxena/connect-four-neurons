def score_(b):
    g = b.grid
    h = b.heights
    s = 0.0
    if 2 <= h[3] <= 5:
        s += 1.5
    if g[2][3] == 1:
        s += 1.5
    if g[1][3] == 1:
        s += 0.5
    if g[0][3] == 2:
        s += 0.5
    s -= 0.25 * sum(h[c] for c in range(7) if c != 3)
    s -= 0.5 * h[4]
    return s

def fires(b):
    return max(0.0, min(1.0, (score_(b) + 2.0) / 5.0))

def level(b):
    return max(0, min(9, int(round(2 * score_(b) + 3))))
