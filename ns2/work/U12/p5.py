def stacked(wins, playable):
    for (r, c) in playable:
        if (r + 1, c) in wins:
            return True
    return False

def level(b):
    mw = b.my_playable_wins
    tw = b.their_playable_wins
    if len(mw) >= 1 and stacked(b.my_wins, mw):
        return 9
    if len(mw) >= 2:
        return 8
    if len(mw) == 1 and b.ply >= 14:
        return 7
    if len(mw) == 0 and len(tw) == 0 and len(b.my_wins) >= 3 and b.ply >= 14:
        return 6
    if len(mw) == 0 and len(tw) >= 2:
        return 5
    if len(mw) == 1:
        return 3
    return 0

def fires(b):
    return level(b) >= 5
