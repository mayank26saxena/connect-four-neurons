def fires(b):
    return any(c == 0 for (r, c) in b.my_wins)

def level(b):
    col0 = [r for (r, c) in b.my_wins if c == 0]
    if not col0:
        return 0
    v = 3 + 2 * (len(col0) - 1)
    if max(col0) >= 2:
        v += 2
    v += len(b.my_wins) - len(col0)
    return min(9, v)
