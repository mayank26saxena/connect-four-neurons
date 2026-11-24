HOT = {(3, 6): 4, (2, 0): 3, (2, 4): 3, (1, 6): 2, (0, 5): 2, (0, 6): 2, (4, 3): 2}

def _k(b):
    if b.last_col is None:
        return 0
    return HOT.get((b.last_row, b.last_col), 0)

def fires(b):
    return _k(b) >= 3

def level(b):
    return 2 * _k(b)
