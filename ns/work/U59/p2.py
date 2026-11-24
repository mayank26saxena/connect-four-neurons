def opening(b):
    return b.ply == 1 and b.last_col in (1, 2, 3, 4, 5)

def later(b):
    if b.ply < 2 or b.ply > 20:
        return False
    if b.my_wins or b.their_wins:
        return False
    return b.grid[0][4] == 2 and b.heights[4] > b.heights[3]

def fires(b):
    return opening(b) or later(b)

def level(b):
    if opening(b):
        return 6 if b.last_col == 4 else 3
    if later(b):
        return 6
    return 0
