def colstack(b, c):
    n = 0
    for r in range(6):
        if b.grid[r][c] == 2:
            n += 1
        else:
            break
    return n

def fires(b):
    return b.grid[0][6] == 2 and b.grid[0][5] == 0 and b.grid[0][4] != 2

def level(b):
    if not fires(b):
        return 0
    return min(9, 3 + 2 * colstack(b, 6))
