def fires(b):
    # early/mid game, all columns open, opponent just played in the centre column
    return b.ply <= 20 and len(b.legal) == 7 and b.last_col == 3

def level(b):
    s = 0
    if len(b.legal) == 7:
        s += 2
    if b.ply <= 20:
        s += 2
    if b.last_col == 3:
        s += 3
    elif b.last_col in (2, 4):
        s += 1
    return min(9, s)
