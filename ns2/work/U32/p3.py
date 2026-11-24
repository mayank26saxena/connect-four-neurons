def total(b):
    L = [0.0, 2.0, 0.0, 0.0, 0.0, 2.0, 0.0]
    W = [2.0, 0.0, 0.5, -0.3, 1.5, -1.5, -0.7]
    V = [-0.7, 0.0, 0.0, -0.3, -0.7, -0.7, 0.0]
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
    t = 0.0
    if b.last_col is not None:
        t += L[b.last_col]
    if nm:
        t += sm / nm
    if no:
        t += so / no
    return t

def fires(b):
    return total(b) >= 2.3

def level(b):
    return max(0, min(9, int(total(b) * 2)))
