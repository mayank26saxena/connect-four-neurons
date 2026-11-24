def fires(b):
    me = [0]*7
    for c in range(7):
        for r in range(6):
            if b.grid[r][c] == 1:
                me[c] += 1
    if b.ply <= 6:
        if b.last_col not in (0, 3, 4):
            return False
        good = me[1] + me[3] + me[5]
        bad = me[4] + me[6]
        return good >= 1 and bad == 0
    if b.last_row == 5 and b.last_col in (0, 3, 6):
        return True
    return False

def level(b):
    if not fires(b):
        return 0
    if b.ply <= 5:
        return 8
    return 5
