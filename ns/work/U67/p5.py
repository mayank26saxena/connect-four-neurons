def wells(b):
    h = b.heights
    out = []
    for c in range(1, 6):
        d = min(h[c - 1], h[c + 1]) - h[c]
        if h[c] <= 1 and d >= 2:
            out.append((c, d))
    return out

def fires(b):
    return len(wells(b)) > 0

def level(b):
    w = wells(b)
    if not w:
        return 0
    s = max(d for c, d in w) + len(w)
    if b.heights[1] == 0:
        s += 2
    return min(9, s)
