def wins_at(g, r, c, p):
    for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
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

def mover_loses(g, h, p, d):
    # True if the player p to move loses by force within d plies
    q = 3 - p
    moves = [c for c in (3, 2, 4, 1, 5, 0, 6) if h[c] < 6]
    if not moves:
        return False
    for c in moves:
        if wins_at(g, h[c], c, p):
            return False
    if d <= 1:
        return False
    # opponent immediate wins: if opponent has a playable win, p must block it
    blocks = [c for c in moves if wins_at(g, h[c], c, q)]
    if len(blocks) >= 2:
        return True
    cand = blocks if blocks else moves
    for c in cand:
        r = h[c]
        g[r][c] = p
        h[c] += 1
        ok = not opp_wins(g, h, q, d - 1)
        h[c] -= 1
        g[r][c] = 0
        if ok:
            return False
    return True

def opp_wins(g, h, q, d):
    # True if q to move can force a win within d plies
    p = 3 - q
    moves = [c for c in (3, 2, 4, 1, 5, 0, 6) if h[c] < 6]
    if not moves:
        return False
    for c in moves:
        if wins_at(g, h[c], c, q):
            return True
    if d <= 2:
        return False
    blocks = [c for c in moves if wins_at(g, h[c], c, p)]
    if len(blocks) >= 2:
        return False
    cand = blocks if blocks else moves
    for c in cand:
        r = h[c]
        g[r][c] = q
        h[c] += 1
        res = mover_loses(g, h, p, d - 1)
        h[c] -= 1
        g[r][c] = 0
        if res:
            return True
    return False

def lost(b, d):
    g = [list(row) for row in b.grid]
    h = list(b.heights)
    return mover_loses(g, h, 1, d)

def fires(b):
    if b.heights[5] != 6:
        return False
    return lost(b, 10)

def level(b):
    if b.heights[5] != 6:
        return 0
    if lost(b, 10):
        return 9 if b.ply >= 32 else 8
    return 2
