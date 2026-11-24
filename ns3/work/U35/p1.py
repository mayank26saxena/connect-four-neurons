def fires(b):
    return len(b.legal) == 1 and b.last_row == 5

def level(b):
    if len(b.legal) == 1 and b.last_row == 5:
        return 9
    if len(b.legal) == 1:
        return 5
    if len(b.legal) == 2 and b.last_row == 5:
        return 4
    return 0
