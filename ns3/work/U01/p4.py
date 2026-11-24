def vert3(b, c, who):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == who for k in range(3))

def col3_threat(b):
    cells = set(b.their_playable_wins) | set(b.my_playable_wins)
    return any(c == 3 for (r, c) in cells)

def fires(b):
    if vert3(b, 3, 2) or vert3(b, 3, 1):
        return True
    if col3_threat(b) and b.ply < 30:
        return True
    if b.my_playable_wins and b.ply < 20:
        return True
    if (vert3(b, 1, 2) or vert3(b, 6, 2)) and b.ply < 30:
        return True
    return False

def level(b):
    if vert3(b, 3, 2):
        return 9 if b.ply < 24 else 7
    if vert3(b, 3, 1):
        return 7
    if col3_threat(b):
        return 6 if b.ply < 30 else 1
    if fires(b):
        return 4
    return 0
