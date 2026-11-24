def fires(b):
    if b.ply == 1:
        return b.last_col in (0, 3, 6)
    # early game: the opponent has just stacked onto column 6 (edge column), second stone or higher
    return b.moves == [6, 6] or b.moves == [6, 6, 6]

def level(b):
    if b.ply == 1:
        return {3: 9, 0: 7, 6: 6, 5: 5, 1: 5, 2: 5, 4: 2}[b.last_col]
    if fires(b):
        return 6
    if b.ply <= 3:
        return 3
    if b.last_row == 5:
        return 3
    return 2
