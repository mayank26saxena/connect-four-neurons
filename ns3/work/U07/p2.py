def fires(b):
    w = b.my_wins
    for r in range(5):
        if (r, 1) in w and (r + 1, 1) in w:
            return True
    return False

def level(b):
    if fires(b):
        return 8
    n1 = len([1 for (r, c) in b.my_wins if c == 1])
    return min(4, 2 * n1)
