def fires(b):
    p = b.ply
    n = len(b.legal)
    if p >= 40:
        return True
    if b.me_first and n <= 1:
        return True
    return b.me_first and p >= 38 and n <= 2

def level(b):
    p = b.ply
    n = len(b.legal)
    if p >= 41:
        return 9
    if p >= 40:
        return 7
    if b.me_first:
        if n <= 1:
            return 6
        if p >= 38 and n <= 2:
            return 4
        if p >= 36 and n <= 3:
            return 2
        return 0
    if p >= 39 and n <= 1:
        return 2
    return 0
