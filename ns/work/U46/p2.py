W = [-0.6, -0.6, 1.0, -0.2, 0.15, -0.6, 0.15]

def share(b):
    if b.ply == 0:
        return 0.0
    return sum(W[c] * b.heights[c] for c in range(7)) / b.ply

def fires(b):
    if b.ply == 1:
        return b.heights[2] == 1
    return b.heights[2] >= 3 and share(b) >= 0.2

def level(b):
    if b.ply == 1:
        return 3 if b.heights[2] == 1 else 0
    if b.heights[2] < 3:
        return 0
    s = share(b) * b.heights[2]
    return max(0, min(9, int(s * 3)))
