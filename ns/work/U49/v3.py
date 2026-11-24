def above_block(b):
    if b.last_col is None:
        return False
    return (b.last_row + 1, b.last_col) in b.their_playable_wins

def fires(b):
    return above_block(b) and b.last_row >= 2

def level(b):
    if not above_block(b):
        return 0
    if b.last_row < 2:
        return 2
    if b.last_col in (1, 4):
        return 8
    return 5
