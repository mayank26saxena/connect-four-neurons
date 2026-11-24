def vthree(b, c):
    # opponent has three stacked on top of column c with the cell above empty
    h = b.heights[c]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    if vthree(b, 5):
        return True
    if b.my_playable_wins:
        return False
    return any(vthree(b, c) for c in (0, 1, 2, 4, 6))

def level(b):
    if vthree(b, 5):
        if b.my_playable_wins:
            return 7
        return 9 if b.last_col == 5 else 8
    if any(vthree(b, c) for c in (0, 1, 2, 4, 6)):
        return 2 if b.my_playable_wins else 5
    if b.their_playable_wins:
        return 2
    return 0
