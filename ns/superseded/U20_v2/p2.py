def fires(b):
    h0, h1 = b.heights[0], b.heights[1]
    if b.my_playable_wins:
        return False
    return (h1 == 2 and h0 < 2) or (h1 == 1 and h0 == 0)

def level(b):
    if not fires(b):
        return 0
    return 6 if b.heights[1] == 2 else 3
