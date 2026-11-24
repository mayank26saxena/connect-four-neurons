def endgame(b):
    h = b.heights
    if h[4] == 6 and h[5] == 6:
        return 0
    left = (h[0] == 6) + (h[1] == 6)
    near = (h[0] >= 5) + (h[1] >= 5)
    if left == 2:
        s = 5
    elif left == 1 and near == 2:
        s = 4
    elif left == 1:
        s = 2
    else:
        s = 0
    s += (h[2] == 6) + (h[3] == 6) + (h[6] == 6)
    s -= 3 * (h[4] == 6) + 2 * (h[5] == 6)
    return max(0, s)

def level(b):
    s = endgame(b)
    if len(b.their_playable_wins) >= 2 and b.ply <= 14:
        s = max(s, 6)
    return min(9, s)

def fires(b):
    return level(b) >= 5
