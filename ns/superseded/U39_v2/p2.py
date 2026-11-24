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
    return 2 * o[3] + h[2] - 2 * (o[1] + o[4] + o[5] + o[6]) - (x[4] + x[6] + x[0])

def fires(b):
    return 7 <= b.ply <= 17 and _s(b) >= 1

def level(b):
    if not (7 <= b.ply <= 17):
        return 0
    return max(0, min(9, _s(b) + 2))
