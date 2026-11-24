def fires(b):
    if b.heights[1] != 3:
        return False
    other = [w for w in (b.my_playable_wins | b.their_playable_wins) if w != (3, 1)]
    return len(other) == 0

def level(b):
    if not fires(b):
        return 0
    if b.last_col == 1:
        return 9
    return 5
