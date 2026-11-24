def strength(b):
    h = b.heights
    left = h[0] + h[1] + h[2] + h[3]
    right = h[4] + h[5] + h[6]
    s = (left - 18) + (1 if h[0] == 6 else 0) - 0.25 * right
    if b.last_col in (4, 5):
        s -= 1.5
    return s

def early(b):
    # early game: two stones of one colour stacked at the bottom of column 0
    if b.ply > 9 or b.heights[0] < 2:
        return False
    return b.grid[0][0] == b.grid[1][0]

def fires(b):
    return strength(b) >= 4.0 or early(b)

def level(b):
    s = strength(b)
    if s >= 6.5:
        return 9
    if s >= 5.5:
        return 7
    if s >= 4.5:
        return 5
    if s >= 4.0 or early(b):
        return 3
    if s >= 3:
        return 1
    return 0
