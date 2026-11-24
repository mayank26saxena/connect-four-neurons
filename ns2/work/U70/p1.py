def fires(b):
    return b.heights[4] == 0 and (1, 4) in b.their_wins

def level(b):
    if fires(b):
        return 9
    return 0
