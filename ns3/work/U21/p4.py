def level(b):
    L = b.last_col
    if L is None:
        return 0
    p = b.ply
    h = b.heights
    if L == 2:
        if p <= 5:
            v = 9
        elif p <= 6:
            v = 8
        elif p <= 10:
            v = 6
        elif p <= 16:
            v = 4
        else:
            v = 3
        if h[3] >= 2 and p <= 10:
            v -= 2
        return v
    if L == 6:
        return {6: 6, 5: 6, 4: 5, 3: 3}.get(h[6], 1)
    if L in (0, 1):
        return 4 if p <= 20 else 2
    if L == 4:
        return 5 if p <= 6 else 2
    if L == 3:
        return 3 if p <= 16 else 1
    return 1

def fires(b):
    return level(b) >= 6
