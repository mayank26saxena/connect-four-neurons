def fires(b):
    empty = sum(1 for c in range(7) if b.heights[c] == 0)
    return empty >= 3

def level(b):
    empty = sum(1 for c in range(7) if b.heights[c] == 0)
    return min(9, empty * 2)
