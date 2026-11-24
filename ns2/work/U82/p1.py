def fires(b):
    # the cell directly on top of the opponent's last stone completes four for the opponent
    c = b.last_col
    if c is None:
        return False
    r = b.last_row + 1
    return (r, c) in b.their_wins

def level(b):
    if not fires(b):
        return 0
    n = len(b.their_playable_wins)
    return 9 if n >= 2 else 7
