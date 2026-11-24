def since_full(b):
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
        return 0.0
    f = b.ply - k
    a = 4.0 - 0.3 * max(0, f - 28)
    if k > 0:
        a -= 1.3
        if k % 2 == 1:
            a -= 0.4
        a -= k * 0.04 * max(0, b.ply - 24)
    return a

def fires(b):
    return est(b) > 1.8

def level(b):
    a = est(b)
    if a <= 0:
        return 1 if b.heights[0] == 5 and b.last_col == 0 else 0
    return max(0, min(9, int(a * 2.2)))
