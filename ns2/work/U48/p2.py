def margin(b):
    left = sum(b.heights[c] for c in range(4))
    right = sum(b.heights[c] for c in range(4, 7))
    return left, right

def fires(b):
    left, right = margin(b)
    return left >= 21 and right <= 10

def level(b):
    left, right = margin(b)
    if left < 19:
        return 0
    s = left - right
    if s >= 20:
        return 9
    if s >= 17:
        return 7
    if s >= 14:
        return 5
    if s >= 11:
        return 3
    return 1
