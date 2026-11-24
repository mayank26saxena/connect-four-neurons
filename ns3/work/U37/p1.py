def fires(b):
    h = b.heights
    low = sum(1 for c in range(7) if h[c] <= 1)
    tall = sum(1 for c in range(7) if h[c] >= 5)
    return low >= 1 and tall >= 3

def level(b):
    h = b.heights
    low = sum(1 for c in range(7) if h[c] <= 1)
    tall = sum(1 for c in range(7) if h[c] >= 5)
    if low == 0:
        return 0
    return min(9, max(0, 2 * tall - 1))
