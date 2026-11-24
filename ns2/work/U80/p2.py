def score_(b):
    g = b.grid
    s = 0.0
    for r in range(6):
        for c in range(7):
            v = g[r][c]
            if v == 2:
                if c == 1 and r <= 4:
                    s += 1
                elif c == 6 and r <= 3:
                    s += 1
                elif c == 5 and r <= 1:
                    s += 0.5
                elif c == 4 and 1 <= r <= 3:
                    s += 0.5
                elif c == 2 or c == 0:
                    s -= 1
            elif v == 1:
                if (r, c) == (0, 0) or (r, c) == (1, 3):
                    s += 1
                elif (r, c) == (0, 3):
                    s += 0.5
                elif c == 1 and 2 <= r <= 4:
                    s += 0.5
                elif c == 2:
                    s -= 0.5
                elif c == 0:
                    s -= 1
    if b.last_col == 1 or b.last_col == 6:
        s += 2
    return s

def fires(b):
    return score_(b) >= 9

def level(b):
    return max(0, min(9, int(score_(b) - 3)))
