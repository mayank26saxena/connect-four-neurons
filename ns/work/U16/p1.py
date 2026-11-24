def fires(b):
    return b.last_col == 0 and b.last_row in (3, 4)

def level(b):
    if b.last_col != 0:
        return 0
    if b.last_row == 4:
        return 8
    if b.last_row == 3:
        return 6
    if b.last_row == 5:
        return 2
    return 0
