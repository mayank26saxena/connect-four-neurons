def fires(b):
    # the opponent has made exactly one move, in any column except the two edge columns
    return b.ply == 1 and b.last_col in (1, 2, 3, 4, 5)

def level(b):
    if b.ply != 1:
        return 0
    return {0: 2, 1: 3, 2: 3, 3: 4, 4: 8, 5: 3, 6: 2}[b.last_col]
