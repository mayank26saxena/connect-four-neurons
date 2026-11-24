def vert6(b):
    h = b.heights[6]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][6] == 2 for k in range(3))

def block6(b):
    return any(c == 6 for (r, c) in b.their_playable_wins)

def fires(b):
    if vert6(b):
        return True
    return block6(b) and b.last_col == 6

def level(b):
    if vert6(b):
        if b.my_playable_wins:
            return 5
        return 9 if b.last_col == 6 else 4
    if block6(b) and b.last_col == 6:
        return 3
    return 0
