LINE = [(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)]

def g(b, r, c):
    return b.grid[r][c]

def fires(b):
    if g(b, 1, 3) != 1:
        return False
    if g(b, 2, 2) == 2 or g(b, 3, 1) == 2:
        return False
    if len(b.my_playable_wins) > 0:
        return False
    other = 0
    if g(b, 3, 1) == 1:
        other += 1
    if g(b, 2, 2) == 1:
        other += 1
    if g(b, 0, 4) == 1:
        other += 1
    if g(b, 4, 0) == 1 and g(b, 0, 4) != 2:
        other += 0
    return other >= 1

def level(b):
    if not fires(b):
        return 0
    n = sum(1 for (r, c) in LINE if g(b, r, c) == 1)
    return 8 if n >= 3 else 6
