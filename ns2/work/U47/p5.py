def fires(b):
    if b.my_playable_wins:
        return False
    if b.heights[1] > 1:
        return False
    tw = b.their_wins
    left = (3, 2) in tw or (2, 2) in tw or (2, 1) in tw
    col0 = any(c == 0 and r >= 2 and r - b.heights[0] <= 1 for (r, c) in tw)
    return left or col0

def level(b):
    if not fires(b):
        return 0
    s = 5
    h2 = b.heights[2]
    if (h2 + 1, 2) in b.their_wins:
        s += 3
    if any(c == 0 for (r, c) in b.their_playable_wins):
        s += 2
    return min(9, s)
