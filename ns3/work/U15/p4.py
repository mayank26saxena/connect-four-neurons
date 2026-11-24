def block_col(b):
    # the single cell I must play to stop an immediate opponent win, or None
    w = list(b.their_playable_wins)
    if len(w) != 1:
        return None
    return w[0]

def fires(b):
    w = block_col(b)
    if w is None:
        return False
    r, c = w
    return (c == 6 and r >= 1) or c == 0

def level(b):
    w = block_col(b)
    if w is None:
        return 0
    r, c = w
    if c == 6 and r >= 1:
        return 8
    if c == 0:
        return 5
    return 3
