def since_full(b):
    # moves played since column 0 received its 6th stone; None if column 0 is not full
    n = 0
    for i, c in enumerate(b.moves):
        if c == 0:
            n += 1
            if n == 6:
                return len(b.moves) - 1 - i
    return None

def est(b):
    k = since_full(b)
    if k is None:
        z = b.heights[0]
        if b.ply <= 10 and z >= 4 and b.last_col == 0 and z * 10 >= 7 * b.ply:
            return 3.0
        if z == 5 and b.last_col == 0:
            return 0.9
        return 0.0
    f = b.ply - k
    if k == 0:
        return 4.0 - 0.3 * max(0, f - 28)
    a1 = 4.0 - 0.3 * max(0, f - 28) - 1.3 - k * 0.04 * max(0, b.ply - 24)
    a2 = min(3.0, 24.0 * (6.0 / b.ply - 0.125))
    a = (a1 + a2) / 2
    if k % 2 == 1:
        a -= 0.4
    return a

def fires(b):
    return est(b) > 1.8

def level(b):
    a = est(b)
    return max(0, min(9, int(a * 2.2)))
