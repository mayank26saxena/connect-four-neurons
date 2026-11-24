def fires(b):
    return b.ply <= 14 and len(b.my_wins) == 0

def level(b):
    if not fires(b):
        return 0
    return 6 if b.ply <= 8 else 4
