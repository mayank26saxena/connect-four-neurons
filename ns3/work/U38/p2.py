def row0_double(b):
    for wins in (b.my_playable_wins, b.their_playable_wins):
        if len([w for w in wins if w[0] == 0]) >= 2:
            return True
    return False

def fires(b):
    return len(b.my_playable_wins) + len(b.their_playable_wins) > 0

def level(b):
    if row0_double(b):
        return 9
    if fires(b):
        return 3
    return 0
