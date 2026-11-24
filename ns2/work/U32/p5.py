def total(b):
    g = [0.1, 1.0, 0.3, 0.3, 0.3, 1.0, 0.5]
    W = [4.0, 0.0, 0.0, 0.0, 2.0, -4.0, 0.0]
    V = [-1.0, 0.0, 0.0, 0.0, -1.0, -2.0, -1.0]
    nm = 0
    no = 0
    sm = 0.0
    so = 0.0
    for c in range(7):
        for r in range(6):
            v = b.grid[r][c]
            if v == 1:
                nm += 1
                sm += W[c]
            elif v == 2:
                no += 1
                so += V[c]
    if b.last_col is None or nm == 0 or no == 0:
        return 0.0
    # the last stone itself is excluded from the opponent share
    so -= V[b.last_col]
    no -= 1
    base = sm / nm + (so / no if no else 0.0)
    return base * g[b.last_col]

def fires(b):
    return total(b) >= 0.7

def level(b):
    return max(0, min(9, int((total(b) + 1.0) * 2.0)))
