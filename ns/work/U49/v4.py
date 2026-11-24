def fires(b):
    if b.last_col != 1 or b.last_row is None:
        return False
    if b.last_row < 1 or b.last_row > 3:
        return False
    return b.heights[2] >= 4 and b.heights[3] >= 4

def level(b):
    s = 0
    if b.last_col == 1 and 1 <= b.last_row <= 3:
        s += 3
    if b.heights[2] >= 4:
        s += 2
    if b.heights[3] >= 4:
        s += 2
    if 2 <= b.heights[1] <= 4:
        s += 1
    return s if s >= 5 else 0
