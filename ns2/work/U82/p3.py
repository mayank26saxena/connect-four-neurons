def stacked(b):
    # opponent has two win cells directly on top of each other in a column
    for (r, c) in b.their_wins:
        if (r + 1, c) in b.their_wins:
            return True
    return False

def score_lost(b):
    pw = b.their_playable_wins
    if len(pw) >= 2:
        return 3
    for (r, c) in pw:
        if (r + 1, c) in b.their_wins:
            return 3
    if pw and stacked(b):
        return 2
    if stacked(b):
        return 2
    if pw:
        return 1
    return 0

def fires(b):
    # the opponent has an unstoppable threat: two immediate wins, or a must-block with another win right above it,
    # or two opponent win cells stacked in one column
    return score_lost(b) >= 2

def level(b):
    return [0, 3, 7, 9][score_lost(b)]
