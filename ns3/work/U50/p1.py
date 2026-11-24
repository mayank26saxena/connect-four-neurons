def fires(b):
    return any(c == 6 for (r, c) in b.my_wins)

def level(b):
    n = sum(1 for (r, c) in b.my_wins if c == 6)
    return min(9, 5 * n)
