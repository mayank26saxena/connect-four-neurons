W = {
    (0, 4): (-1.5, 2.0), (1, 4): (-1.0, 1.0), (0, 3): (-2.0, 1.5), (1, 3): (-1.0, 1.0),
    (0, 2): (1.5, 0.0), (1, 2): (0.0, 1.0), (2, 2): (0.5, 0.0),
}

def score(b):
    g = b.grid
    s = 0.0
    for (r, c), (wm, wt) in W.items():
        if g[r][c] == 1:
            s += wm
        elif g[r][c] == 2:
            s += wt
    s -= 0.5 * (b.heights[0] + b.heights[1])
    s -= 0.15 * b.ply
    if b.ply % 2 == 1:
        s -= 1.0
    return s

def fires(b):
    v = score(b)
    return max(0.0, min(1.0, (v + 1.0) / 6.0))

def level(b):
    v = score(b)
    return max(0, min(9, int(round(v * 1.5))))
