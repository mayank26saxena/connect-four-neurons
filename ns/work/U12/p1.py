def depth(b):
    best = 0
    for c in range(1, 6):
        h = b.heights[c]
        d = min(b.heights[c - 1], b.heights[c + 1]) - h
        if d > best:
            best = d
    return best

def fires(b):
    return depth(b) >= 2

def level(b):
    return min(9, depth(b) * 2)
