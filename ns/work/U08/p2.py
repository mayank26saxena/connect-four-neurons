def nfull(b):
    return sum(1 for c in range(7) if b.heights[c] == 6)

def fires(b):
    return b.last_col == 5 and b.heights[5] <= 5 and nfull(b) >= 3

def level(b):
    f = nfull(b)
    h5 = b.heights[5]
    if b.last_col == 5:
        if h5 == 6:
            return 0
        if f >= 5:
            return 9 if h5 <= 4 else 7
        if f >= 3:
            return 7 if h5 <= 4 else 5
        if f >= 1:
            return 4
        return 2
    if b.last_col in (2, 4, 6) and f >= 3 and 1 <= h5 <= 4:
        return 3
    return 0
