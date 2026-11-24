def score_(b):
    g = b.grid
    s = 0.0
    # center column built up with my stone in the third cell
    if g[2][3] == 1:
        s += 2
    if g[1][3] != 0:
        s += 1
    # right-of-center column empty
    s -= 0.7 * b.heights[4]
    if g[0][4] == 2:
        s -= 1
    # their stones low on the left, mine absent there
    s += 0.5 * sum(1 for c in (0, 1, 2) if g[0][c] == 2)
    s -= 0.5 * sum(1 for c in (0, 1, 2) for r in (0, 1, 2) if g[r][c] == 1)
    # fewer stones overall
    s -= 0.08 * b.ply
    return s

def fires(b):
    s = score_(b)
    return max(0.0, min(1.0, (s + 1.0) / 4.0))

def level(b):
    return max(0, min(9, int(round(2 * score_(b) + 2))))
