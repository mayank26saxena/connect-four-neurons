def vthree6(b):
    h = b.heights[6]
    if h < 3 or h >= 6:
        return 0
    if all(b.grid[h - 1 - k][6] == 2 for k in range(3)):
        return h
    return 0

def block6(b):
    # a must-block cell in column 6 above the bottom row (any direction)
    return any(c == 6 and r >= 1 for (r, c) in b.their_playable_wins)

def fires(b):
    return vthree6(b) > 0 or block6(b)

def level(b):
    h = vthree6(b)
    if h:
        v = {3: 9, 4: 7, 5: 6}[h]
        if b.my_playable_wins:
            v -= 3
        return v
    if block6(b):
        return 4
    h = b.heights[6]
    if b.last_col == 6 and h >= 2 and b.grid[h - 2][6] == 2:
        return 2
    if b.last_col == 6:
        return 1
    return 0
