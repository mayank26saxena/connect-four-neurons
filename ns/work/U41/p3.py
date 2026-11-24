def fires(b):
    # only the empty starting board
    return b.ply == 0

def level(b):
    if b.ply == 0:
        return 9
    if b.ply == 1:
        return 0 if b.moves[0] == 2 else 2
    if b.ply == 2:
        return 1
    if b.ply <= 4:
        return 1
    return 0
