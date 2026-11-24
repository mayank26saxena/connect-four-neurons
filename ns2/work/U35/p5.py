LAST = [0.0, 0.4, 0.05, 0.4, 0.6, 0.65, 0.9]
W = [-0.35, 0.0, -0.35, -0.05, 0.08, 0.08, 0.12]

def score(b):
    if b.last_col is None:
        return -9.0
    s = LAST[b.last_col] - 0.15 * max(0, b.last_row - 1)
    s += sum(W[c] * b.heights[c] for c in range(7))
    s -= 0.025 * b.ply
    return s

def fires(b):
    return score(b) > 0.45

def level(b):
    s = score(b)
    return max(0, min(9, int((s - 0.1) / 0.1)))
