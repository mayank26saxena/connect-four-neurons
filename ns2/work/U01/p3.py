def fires(b):
    # my stone in the bottom-left corner and their stone in the bottom-right corner
    return b.grid[0][0] == 1 and b.grid[0][6] == 2

def level(b):
    if not fires(b):
        return 0
    s = 4
    if b.grid[2][4] == 2:
        s += 2
    if b.grid[1][2] == 2 or b.grid[1][1] == 2:
        s += 2
    if b.ply <= 12:
        s += 1
    return min(9, s)
