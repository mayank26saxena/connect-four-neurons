def opening(b):
    return b.ply == 1 and b.last_col in (1, 2, 3, 4, 5)

def later(b):
    if b.ply < 3 or b.ply > 12:
        return False
    if b.my_wins or b.their_wins:
        return False
    return b.last_col == 4 and b.heights[4] > b.heights[3]

def fires(b):
    return opening(b) or later(b)

def level(b):
    if b.ply == 1:
        return {0: 3, 1: 4, 2: 4, 3: 5, 4: 7, 5: 4, 6: 3}[b.last_col]
    if later(b):
        return 5
    return 0
