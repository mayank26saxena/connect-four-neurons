W = {(0, 2): 6, (0, 4): 6, (5, 4): 5, (1, 6): 5, (4, 4): 3, (5, 2): 3, (1, 1): 3}

def fires(b):
    if b.last_col is None:
        return False
    return (b.last_row, b.last_col) in ((0, 2), (0, 4), (5, 4), (1, 6))

def level(b):
    if b.last_col is None:
        return 0
    return W.get((b.last_row, b.last_col), 0)
