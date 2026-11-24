def fires(b):
    # early game, I own a bottom corner cell, and the center bottom is not mine
    edge = (b.grid[0][0] == 1) + (b.grid[0][6] == 1)
    return b.ply <= 12 and edge >= 1 and b.grid[0][3] != 1

def level(b):
    if not fires(b):
        return 0
    edge = (b.grid[0][0] == 1) + (b.grid[0][6] == 1)
    return 4 + 2 * edge
