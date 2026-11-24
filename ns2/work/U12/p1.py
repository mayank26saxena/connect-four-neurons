def stacked(wins, playable):
    # a playable winning cell with another winning cell directly above it
    for (r, c) in playable:
        if (r + 1, c) in wins:
            return True
    return False

def fires(b):
    mw = b.my_playable_wins
    tw = b.their_playable_wins
    if len(mw) >= 2:
        return True
    if len(mw) == 1 and (b.ply >= 18 or stacked(b.my_wins, mw)):
        return True
    if len(mw) == 0 and len(tw) >= 2:
        return True
    return False

def level(b):
    mw = b.my_playable_wins
    if not fires(b):
        return 0
    if len(mw) == 0:
        return 4
    if b.ply >= 24:
        return 9
    return 7
