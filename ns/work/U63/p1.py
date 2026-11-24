def fires(b):
    return b.ply == 1 and b.last_col in (0, 5, 6)

def level(b):
    if b.ply == 1:
        return {6: 9, 5: 6, 0: 3, 3: 3, 4: 3, 1: 2}.get(b.last_col, 0)
    return 0
