def fires(b):
    return (not b.me_first) and b.last_col in (4, 5)

def level(b):
    if b.me_first or b.last_col not in (4, 5):
        return 0
    if b.ply == 1:
        return 9 if b.last_col == 5 else 7
    return 4 if b.last_col == 5 else 3
