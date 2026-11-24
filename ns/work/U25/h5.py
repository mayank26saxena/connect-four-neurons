def makes_four(g, r, c, p):
    for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
        n = 1
        for s in (1, -1):
            rr = r + s * dr
            cc = c + s * dc
            while 0 <= rr < 6 and 0 <= cc < 7 and g[rr][cc] == p:
                n += 1
                rr += s * dr
                cc += s * dc
        if n >= 4:
            return True
    return False

def solve(g, h, p, empty):
    # value for player p to move: 1 win, 0 draw, -1 loss
    if empty == 0:
        return 0
    cols = [c for c in (3, 2, 4, 1, 5, 0, 6) if h[c] < 6]
    for c in cols:
        if makes_four(g, h[c], c, p):
            return 1
    q = 3 - p
    best = -1
    for c in cols:
        r = h[c]
        g[r][c] = p
        h[c] += 1
        v = -solve(g, h, q, empty - 1)
        h[c] -= 1
        g[r][c] = 0
        if v > best:
            best = v
            if best == 1:
                return 1
    return best

def value(b):
    empty = 42 - b.ply
    if empty > 12:
        return None
    g = [list(row) for row in b.grid]
    h = list(b.heights)
    return solve(g, h, 1, empty)

def fires(b):
    if b.ply <= 9:
        return len(b.their_playable_wins) >= 2 or len(b.my_playable_wins) >= 2
    v = value(b)
    if v is None:
        return False
    return v == -1

def level(b):
    if b.ply <= 9:
        return 8 if fires(b) else 0
    v = value(b)
    if v is None:
        return 1 if b.ply >= 26 else 0
    if v == -1:
        return 9 if len(b.legal) <= 2 else 7
    if v == 0:
        return 5 if len(b.legal) <= 1 else 3
    return 2
