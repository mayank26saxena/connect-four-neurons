def fires(b):
    if b.grid[0][4] == 1:
        return False
    return any(c <= 4 for (r, c) in b.their_wins)

def level(b):
    if not fires(b):
        return 0
    n = len([1 for (r, c) in b.their_wins if c <= 4])
    return min(9, 3 + 2 * n)
