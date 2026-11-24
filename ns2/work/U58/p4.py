W = {(1, 6): 5, (3, 1): 5, (0, 4): 4, (3, 5): 4, (2, 0): 4, (2, 3): 3}

def fires(b):
    # the opponent's last stone landed in row 4 (fifth stone) of column 2
    return b.last_col == 2 and b.last_row == 4

def level(b):
    if b.last_col is None:
        return 0
    if fires(b):
        return 8 if b.ply % 2 == 0 else 6
    return W.get((b.last_row, b.last_col), 1)
