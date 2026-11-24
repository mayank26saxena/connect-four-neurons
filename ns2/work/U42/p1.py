def fires(b):
    return b.last_col == 0 and b.last_row >= 3

def level(b):
    if b.last_col != 0:
        return 0
    return [0, 1, 3, 5, 7, 9][b.last_row]
