DIRS = ((0, 1), (1, 0), (1, 1), (1, -1))

def wins_at(g, r, c, p):
    for dr, dc in DIRS:
        n = 1
        for s in (1, -1):
            rr, cc = r + s * dr, c + s * dc
            while 0 <= rr < 6 and 0 <= cc < 7 and g[rr][cc] == p:
                n += 1
                rr += s * dr
                cc += s * dc
        if n >= 4:
            return True
    return False

def playable_wins(g, h, p):
    out = []
    for c in range(7):
        if h[c] < 6 and wins_at(g, h[c], c, p):
            out.append((h[c], c))
    return out

def best_double(b):
    if b.my_playable_wins or b.their_playable_wins:
        return 0
    best = 0
    for c in b.legal:
        g = [row[:] for row in b.grid]
        h = list(b.heights)
        r = h[c]
        g[r][c] = 1
        h[c] += 1
        n = len(playable_wins(g, h, 1))
        best = max(best, n)
    return best

def fires(b):
    return best_double(b) >= 2

def level(b):
    return 8 if fires(b) else 0
