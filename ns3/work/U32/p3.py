def col1_threat(b):
    return any(c == 1 and r >= 2 for (r, c) in b.my_wins) or any(c == 1 and r >= 2 for (r, c) in b.their_wins)

def fires(b):
    if b.heights[1] != 1:
        return False
    return b.grid[3][3] == 2 or col1_threat(b)

def level(b):
    if b.heights[1] != 1:
        return 0
    s = 2
    if b.grid[3][3] == 2: s += 3
    if col1_threat(b): s += 3
    if b.heights[0] >= 1: s += 1
    return s
