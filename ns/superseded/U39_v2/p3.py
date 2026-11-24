def _s(b):
    n = len(b.moves)
    o = [0] * 7
    x = [0] * 7
    for i, c in enumerate(b.moves):
        if i % 2 == n % 2:
            x[c] += 1
        else:
            o[c] += 1
    h = b.heights
    g = b.grid
    s = 2 * o[3] + h[2] - 2 * (o[1] + o[4] + o[5] + o[6]) - (x[4] + x[6] + x[0])
    s += {0: 2, 1: -3, 2: -3, 3: 0, 4: 0, 5: 0, 6: 2}[b.last_col]
    s += 2 * (g[0][3] == 2) + 2 * (g[0][5] == 1) - 2 * (h[4] >= 2) - (h[5] >= 2) - (h[6] >= 2)
    return s

def fires(b):
    return 7 <= b.ply <= 17 and _s(b) >= 4

def level(b):
    if b.ply < 4 or b.ply > 20:
        return 0
    return max(0, min(9, _s(b)))
