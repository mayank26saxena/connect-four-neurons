def fires(b):
    r = b.landing(5)
    return r is not None and r + 1 < 6 and (r + 1, 5) in b.their_wins

def level(b):
    return 8 if fires(b) else 0
