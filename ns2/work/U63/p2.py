def fires(b):
    # early game, opponent stone sitting on my stone in the bottom-left corner
    return b.ply <= 12 and b.grid[0][0] == 1 and b.grid[1][0] == 2

def level(b):
    if not (b.grid[0][0] == 1 and b.grid[1][0] == 2):
        return 0
    return max(0, 9 - max(0, b.ply - 4))
