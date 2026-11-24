def vert_three(b, c, who):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == who for k in range(3))

def fires(b):
    return vert_three(b, 0, 2) or vert_three(b, 0, 1)

def level(b):
    if vert_three(b, 0, 2):
        return 9 if b.last_col == 0 else 7
    if vert_three(b, 0, 1):
        return 5
    if any(vert_three(b, c, 2) for c in range(1, 7)):
        return 3
    if b.their_playable_wins:
        return 2
    return 0
