def fires(b):
    n = len(b.legal)
    if b.ply >= 41:
        return True
    return b.me_first and n <= 2

def level(b):
    n = len(b.legal)
    if b.ply >= 41:
        return 9
    if b.me_first:
        if n <= 1:
            return 8
        if n == 2:
            return 5
        if n == 3:
            return 2
        return 0
    if n <= 1:
        return 1
    return 0
