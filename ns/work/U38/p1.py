def fires(b):
    return b.grid[0][6] == 1 and b.ply <= 9

def level(b):
    if b.grid[0][6] != 1:
        return 0
    if b.ply <= 3:
        return 6
    if b.ply <= 7:
        return 8
    if b.ply <= 9:
        return 5
    if b.ply <= 13:
        return 2
    return 1
