BASE = [0.0, 0.4, 2.0, 2.8, 3.0, 3.0, 3.0]

def nth(b, c):
    return sum(1 for r in range(6) if b.grid[r][c] == 2)

def since4(b):
    m = b.moves
    k = 0
    i = len(m) - 1
    while i >= 0:
        if m[i] == 4:
            return k
        k += 1
        i -= 2
    return 99

def score(b):
    n = nth(b, 4)
    s = BASE[n]
    s -= 0.4 * max(0, since4(b) - 1)
    s -= 0.3 * (b.heights[3] + b.heights[5])
    if b.last_col == 4 and b.last_row >= 2 and any(b.grid[r][4] == 1 for r in range(6)):
        s -= 1.5
    return s

def fires(b):
    return score(b) >= 0.9

def level(b):
    return max(0, min(9, int(round(score(b) * 3))))
