def fires(b):
    return b.last_col == 2 and b.last_row == 4

def level(b):
    return 7 if fires(b) else 0
