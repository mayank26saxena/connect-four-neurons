W = [1.0, 1.0, 0.8, 0.8, 0.6, 0.6, 0.4, 0.4, 0.2, 0.2]

def nth(b, c):
    return sum(1 for r in range(6) if b.grid[r][c] == 2)

def tok(b):
    m = b.moves
    s = 0.0
    for k in range(min(len(m), len(W))):
        c = m[len(m) - 1 - k]
        if c == 4 and k % 2 == 0:
            s += W[k]
        elif c == 3 or c == 5:
            s -= W[k]
    return s

def fires(b):
    return nth(b, 4) >= 2 and tok(b) >= 1.0

def level(b):
    if nth(b, 4) < 2:
        return 1 if tok(b) >= 1.0 else 0
    s = tok(b) + 0.5 * min(nth(b, 4), 4) - 0.5 * b.heights[5]
    return max(0, min(9, int(round(3 * s))))
