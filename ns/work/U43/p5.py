def tall(b):
    return sum(1 for c in range(6) if b.heights[c] >= 4)

def fires(b):
    if b.heights[6] != 3:
        return False
    t = tall(b)
    return t >= 4 or (t == 3 and b.last_col != 6)

def level(b):
    if b.heights[6] != 3:
        return 0
    v = 1 + 2 * tall(b)
    if b.last_col == 6:
        v -= 2
    return max(1, min(9, v))
