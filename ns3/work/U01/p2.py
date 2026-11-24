def vert3(b, c, who):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == who for k in range(3))

def fires(b):
    cells = set(b.their_playable_wins) | set(b.my_playable_wins)
    return any(c == 3 for (r, c) in cells)

def level(b):
    cells = set(b.their_playable_wins) | set(b.my_playable_wins)
    if vert3(b, 3, 2):
        return 9
    if vert3(b, 3, 1):
        return 7
    if any(c == 3 for (r, c) in cells):
        return 6
    if cells:
        return 2
    return 0
