def fires(b):
    n = len(b.legal)
    if n == 1:
        return True
    return n == 2 and b.last_row == 5 and b.ply >= 30

def level(b):
    n = len(b.legal)
    if n == 1:
        return 9 if b.last_row == 5 else 6
    if n == 2:
        return 5 if b.last_row == 5 else 2
    if n == 3 and b.last_row == 5:
        return 1
    return 0
