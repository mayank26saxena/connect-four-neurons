W = {(1, 6): 4, (3, 1): 4, (0, 4): 4, (3, 5): 4, (2, 0): 3}

def fires(b):
    if b.last_col is None:
        return False
    if b.last_col == 2 and b.last_row == 4:
        return True
    # opponent answered directly on top of my stone in column 6 (second stone there)
    return b.last_col == 6 and b.last_row == 1 and len(b.moves) >= 2 and b.moves[-2] == 6

def level(b):
    if b.last_col is None:
        return 0
    if b.last_col == 2 and b.last_row == 4:
        return 8
    if fires(b):
        return 6
    return W.get((b.last_row, b.last_col), 1)
