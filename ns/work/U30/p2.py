def fires(b):
    if b.heights[1] != 1:
        return False
    full = sum(1 for c in range(7) if b.heights[c] == 6)
    return full >= 1 or b.last_col == 1

def level(b):
    if b.heights[1] != 1:
        return 0
    full = sum(1 for c in range(7) if b.heights[c] == 6)
    s = 2 + 2 * min(full, 3)
    if b.last_col == 1:
        s += 2
    return min(9, s)
