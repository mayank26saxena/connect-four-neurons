def fires(b):
    return b.ply == 0

def level(b):
    if b.ply == 0:
        return 9
    if b.ply == 1:
        return 2
    if b.ply <= 4:
        return 1
    return 0
