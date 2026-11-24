def col0_gap(b):
    # smallest distance between column 0's landing cell and one of my winning cells in column 0
    h = b.landing(0)
    if h is None:
        return None
    ds = [r - h for (r, c) in b.my_wins if c == 0]
    return min(ds) if ds else None

def fires(b):
    d = col0_gap(b)
    return d is not None and d <= 1

def level(b):
    d = col0_gap(b)
    if d is None:
        return 0
    n = len(b.my_wins)
    if d == 0:
        v = 6
    elif d == 1:
        v = 4
    elif d == 2:
        v = 1
    else:
        return 0
    v += min(3, n - 1)
    return min(9, v)
