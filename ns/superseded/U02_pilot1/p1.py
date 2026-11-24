def fires(b):
    # opponent's opening move (one stone on the board) in column 0, 3 or 6
    return b.ply == 1 and b.last_col in (0, 3, 6)

def level(b):
    if b.ply == 1:
        return {3: 9, 0: 6, 6: 5, 5: 4, 1: 4, 2: 4, 4: 1}[b.last_col]
    return 1
