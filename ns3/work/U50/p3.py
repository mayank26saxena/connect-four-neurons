def fires(b):
    cells = list(b.my_wins) + list(b.their_wins)
    return any(c in (2, 6) for (r, c) in cells)

def level(b):
    n = sum(1 for (r, c) in b.my_wins if c in (2, 6)) * 2 + sum(1 for (r, c) in b.their_wins if c in (2, 6))
    return min(9, 2 * n)
