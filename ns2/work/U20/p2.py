def parity_threat(b):
    want = 0 if not b.me_first else 1
    return any(r % 2 == want for (r, c) in b.their_wins)

def fires(b):
    return b.heights[4] == 6 and parity_threat(b)

def level(b):
    if b.heights[4] < 6:
        return 0
    s = 3 if parity_threat(b) else 1
    s += 2 * (b.heights[5] == 6) + 2 * (b.heights[3] == 6)
    return min(9, s)
