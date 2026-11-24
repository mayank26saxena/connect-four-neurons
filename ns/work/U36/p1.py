def fires(b):
    return b.ply == 0

def level(b):
    return 9 if b.ply == 0 else 0
