def fires(b):
    p = b.ply
    n = len(b.legal)
    if p >= 41:
        return True
    if b.me_first:
        if p >= 38:
            return True
        if p >= 34:
            return n <= 2
        return False
    return p >= 37 and n <= 1

def level(b):
    p = b.ply
    n = len(b.legal)
    if p >= 41:
        return 9
    if b.me_first:
        s = 0
        if p >= 40:
            s = 6
        elif p >= 38:
            s = 4
        elif p >= 36:
            s = 2
        elif p >= 34:
            s = 1
        if n <= 1:
            s += 3
        elif n == 2:
            s += 1
        return min(s, 9)
    if p >= 37 and n <= 1:
        return 3
    if p >= 37 and n == 2:
        return 1
    return 0
