def score_(b):
    if b.my_playable_wins:
        return 0
    s = 0
    h1 = b.heights[1]
    if h1 <= 1:
        s += 2
    elif h1 < 6:
        s -= 3
    if b.last_row == 2:
        s += 1
    if (3, 2) in b.their_wins or (b.heights[2] + 1, 2) in b.their_wins:
        s += 2
    if any(c in (0, 1, 5, 6) for (r, c) in b.their_playable_wins):
        s += 2
    if any(c in (0, 2) for (r, c) in b.their_wins):
        s += 1
    return s

def fires(b):
    return score_(b) >= 4

def level(b):
    return max(0, min(9, 2 * score_(b) - 2))
