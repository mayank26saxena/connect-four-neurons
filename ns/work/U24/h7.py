HS = [0.0, 0.0, 0.75, 1.2, 1.0, -0.5, -2.0]

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
    h = b.heights[4]
    n = nth(b, 4)
    s = HS[h] + 0.8 * min(n, 3)
    s -= 0.6 * min(6, max(0, since4(b) - 1))
    s -= 0.3 * (b.heights[3] + b.heights[5])
    s -= 0.05 * max(0, b.ply - 8)
    if b.last_col == 4:
        r = b.last_row
        if r >= 3 or (r >= 2 and any(b.grid[k][4] == 1 for k in range(r))):
            s -= 2.0
    return s

def fires(b):
    return score(b) >= 1.3

def level(b):
    return max(0, min(9, int(round(score(b) * 3))))
