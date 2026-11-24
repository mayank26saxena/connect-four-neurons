def fires(b):
    return b.ply <= 8

def level(b):
    if b.ply <= 6:
        return 6
    if b.ply <= 10:
        return 3
    return 0
