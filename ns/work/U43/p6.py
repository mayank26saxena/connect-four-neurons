W = [0.5, 1.0, 1.0, 1.5, 2.0, 1.0]

def tallw(b):
    return sum(W[c] for c in range(6) if b.heights[c] >= 4)

def fires(b):
    return b.heights[6] == 3 and tallw(b) >= 3.5 and b.last_col != 6 or (b.heights[6] == 3 and tallw(b) >= 5)

def level(b):
    if b.heights[6] != 3:
        return 0
    v = 1 + tallw(b) * 1.2
    if b.last_col == 6:
        v -= 2
    return int(max(1, min(9, v)))
