def fires(b):
    h = b.heights
    if h[6] < 6:
        return False
    nfull = sum(1 for c in range(7) if h[c] == 6)
    return nfull >= 3 and h[2] <= 3

def level(b):
    h = b.heights
    if h[6] < 6:
        return 0
    nfull = sum(1 for c in range(7) if h[c] == 6)
    s = nfull + (2 if h[2] <= 1 else (1 if h[2] <= 3 else 0))
    return min(9, s)
