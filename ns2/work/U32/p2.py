def sig(b):
    wm = [1.0, 0.0, 0.2, 0.0, 1.0, -1.0, -0.5]
    wo = [1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0]
    nm = 0
    no = 0
    sm = 0.0
    so = 0.0
    for c in range(7):
        for r in range(6):
            v = b.grid[r][c]
            if v == 1:
                nm += 1
                sm += wm[c]
            elif v == 2:
                no += 1
                so += wo[c]
    if nm == 0 or no == 0:
        return 0.0
    return sm / nm - 0.5 * so / no

def fires(b):
    if b.last_col not in (1, 5):
        return False
    return sig(b) >= 0.3

def level(b):
    if b.last_col not in (1, 5):
        return 0
    return max(0, min(9, int(sig(b) * 12)))
