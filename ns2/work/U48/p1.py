def fires(b):
    left = sum(b.heights[c] for c in range(4))
    return left >= 22

def level(b):
    left = sum(b.heights[c] for c in range(4))
    if left >= 24:
        return 8
    if left >= 22:
        return 5
    if left >= 20:
        return 2
    return 0
