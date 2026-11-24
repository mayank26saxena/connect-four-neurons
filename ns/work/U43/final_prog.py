def tall(b):
    # columns 0-5 holding at least 4 stones
    return sum(1 for c in range(6) if b.heights[c] >= 4)

def fires(b):
    return b.heights[6] == 3 and tall(b) >= 3

def level(b):
    if b.heights[6] != 3:
        return 0
    v = 1 + 2 * tall(b)
    if b.last_col == 6:
        v -= 2
    return max(1, min(9, v))
