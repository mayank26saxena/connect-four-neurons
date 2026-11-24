def vthreat(b, c):
    # opponent has three stacked at the top of column c and the cell above is empty (a must-block)
    h = b.heights[c]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    if b.my_playable_wins:
        return False
    return any(vthreat(b, c) for c in (0, 2, 4))

def level(b):
    if b.my_playable_wins:
        return 0
    if vthreat(b, 0) or vthreat(b, 2):
        return 9
    if vthreat(b, 4):
        return 6
    return 0
