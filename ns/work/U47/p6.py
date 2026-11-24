def fires(b):
    if b.heights[1] != 3:
        return False
    urgent = b.my_playable_wins | b.their_playable_wins
    if (3, 1) in urgent:
        return True
    if urgent:
        return False
    return b.ply >= 12

def level(b):
    if b.heights[1] != 3:
        return 0
    urgent = b.my_playable_wins | b.their_playable_wins
    if (3, 1) in urgent:
        return 9
    if urgent:
        return 1
    v = 3
    if b.ply >= 12:
        v += 2
    if b.last_col == 1:
        v += 3
    return v
