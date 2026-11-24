def fires(b):
    return b.ply == 1 and b.last_col in (3, 4, 5)

def level(b):
    if b.ply == 1:
        return {5: 9, 3: 6, 4: 5, 0: 2, 1: 2}.get(b.last_col, 0)
    return 0
