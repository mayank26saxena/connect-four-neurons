def fires(b):
    if b.ply >= 41:
        return True
    return b.me_first and b.ply >= 36

def level(b):
    p = b.ply
    if p >= 41:
        return 9
    if b.me_first:
        if p >= 40:
            return 8
        if p >= 38:
            return 6
        if p >= 36:
            return 4
        if p >= 34:
            return 2
        return 0
    if p >= 37:
        return 2
    return 0
