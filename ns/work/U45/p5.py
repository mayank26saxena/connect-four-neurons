def gap(b):
    # an empty column 2 or 3 with stones on both sides of it
    h = b.heights
    for c in (2, 3):
        if h[c] == 0 and max(h[:c]) > 0 and max(h[c + 1:]) > 0:
            return c
    return None

def fires(b):
    if b.ply < 7 or b.ply > 24:
        return False
    if b.my_playable_wins or b.their_playable_wins:
        return False
    return gap(b) is not None

def level(b):
    if not fires(b):
        return 0
    c = gap(b)
    s = 4
    if c == 2:
        s += 1
        if b.heights[1] == 0:
            s += 1
    if b.ply <= 14:
        s += 1
    return s
