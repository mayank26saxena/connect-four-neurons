def fires(b):
    p = b.ply
    n = len(b.legal)
    if p >= 40:
        return True
    if b.me_first and p >= 34 and n <= 2:
        return True
    return p >= 39 and n <= 1

def level(b):
    p = b.ply
    n = len(b.legal)
    if p >= 41:
        return 9
    if p >= 40:
        return 7
    if b.me_first:
        if p >= 34 and n <= 1:
            return 6
        if p >= 34 and n <= 2:
            return 4
        if p >= 34 and n <= 3:
            return 2
        return 0
    if p >= 39 and n <= 1:
        return 3
    return 0
