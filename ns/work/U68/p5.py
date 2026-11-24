def vthreat(b, c):
    # opponent has three stacked at the top of column c and the cell above is empty (a must-block)
    h = b.heights[c]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    if b.my_playable_wins:
        return False
    return vthreat(b, 0) or vthreat(b, 2) or (vthreat(b, 4) and not b.me_first)

def level(b):
    if b.my_playable_wins:
        return 0
    if vthreat(b, 0) or vthreat(b, 2):
        return 9
    if vthreat(b, 4) and not b.me_first:
        return 6
    return 0
