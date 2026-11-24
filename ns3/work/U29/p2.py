def fires(b):
    for c in b.legal:
        l = b.landing(c)
        if l < 5 and ((l + 1, c) in b.my_wins or (l + 1, c) in b.their_wins):
            return True
    return False

def level(b):
    return 5 if fires(b) else 0
