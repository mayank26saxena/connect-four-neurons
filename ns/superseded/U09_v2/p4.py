OW = {(2, 2): 2.0, (1, 2): 1.0, (1, 3): 1.0, (0, 2): 0.7, (0, 3): 0.7,
      (2, 1): 0.7, (1, 1): 0.7, (3, 1): 0.7, (0, 1): 0.5}
XW = {(2, 2): 1.5, (1, 2): 1.0, (1, 3): 1.0, (0, 4): 1.6, (2, 3): 0.7,
      (0, 1): 0.5, (3, 2): 0.5}

def score(b):
    g = b.grid
    s = 0.0
    for (r, c), w in OW.items():
        if g[r][c] == 2:
            s += w
    for (r, c), w in XW.items():
        if g[r][c] == 1:
            s -= w
    for r0 in (0, 1):
        if all(g[r0 + k][2] == 2 for k in range(3)) and g[r0 + 3][2] == 0:
            s += 1.5
    return s

def fires(b):
    return score(b) >= 3.0

def level(b):
    s = score(b)
    if s < 1.0:
        return 0
    return max(0, min(9, int(round((s - 1.0) * 2))))
