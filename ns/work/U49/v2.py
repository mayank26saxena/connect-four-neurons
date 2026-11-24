HOT = {(2, 1): 6, (3, 1): 6, (3, 4): 6, (3, 0): 3, (1, 0): 3, (3, 5): 3, (4, 5): 3, (4, 3): 3, (4, 4): 3, (3, 6): 3, (4, 6): 3}

def fires(b):
    if b.last_col is None:
        return False
    return HOT.get((b.last_row, b.last_col), 0) >= 6

def level(b):
    if b.last_col is None:
        return 0
    return HOT.get((b.last_row, b.last_col), 0)
