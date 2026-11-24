def fires(b):
    l = b.landing(3)
    if l is None:
        return b.ply >= 12
    if l + 1 <= 5 and ((l + 1, 3) in b.my_wins or (l + 1, 3) in b.their_wins):
        return True
    return False

def level(b):
    return 5 if fires(b) else 0
