def vert3(b):
    c = b.last_col
    if c is None:
        return False
    r = b.last_row
    return (r + 1, c) in b.their_playable_wins and r >= 2 and b.grid[r-1][c] == 2 and b.grid[r-2][c] == 2

def fires(b):
    if vert3(b) and b.last_col in (0, 2, 4):
        return True
    return any(c == 0 for (r, c) in b.their_playable_wins)

def level(b):
    if vert3(b) and b.last_col in (0, 2):
        return 9
    if fires(b):
        return 6
    return 0
