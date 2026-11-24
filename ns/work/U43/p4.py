def tall(b):
    return sum(1 for c in range(6) if b.heights[c] >= 4)

def fires(b):
    return b.heights[6] == 3 and tall(b) >= 3

def level(b):
    if b.heights[6] != 3:
        return 0
    return min(9, 1 + 2 * tall(b))
