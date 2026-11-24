def fires(b):
    return len(b.my_wins) >= 2

def level(b):
    return min(9, 2 * len(b.my_wins))
