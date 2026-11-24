def fires(b):
    return b.ply == 1 and b.last_col != 6

def level(b):
    if b.ply == 1:
        return {0: 7, 1: 4, 2: 4, 3: 4, 4: 6, 5: 9, 6: 2}[b.last_col]
    return 0
