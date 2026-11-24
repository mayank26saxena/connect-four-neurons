W = {(4, 2): 8, (1, 6): 5, (3, 1): 5, (0, 4): 5, (3, 5): 5, (2, 0): 4}

def fires(b):
    if b.last_col is None:
        return False
    return (b.last_row, b.last_col) in W

def level(b):
    if b.last_col is None:
        return 0
    return W.get((b.last_row, b.last_col), 1)
