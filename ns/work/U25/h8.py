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

def move_values(b):
    # value (for me) of each legal move, by exact search; None if too many empty cells
    empty = 42 - b.ply
    if empty > 16 or (empty > 12 and len(b.legal) > 3):
        return None
    g = [list(row) for row in b.grid]
    h = list(b.heights)
    out = []
    for c in b.legal:
        r = h[c]
        if makes_four(g, r, c, 1):
            out.append(1)
            continue
        g[r][c] = 1
        h[c] += 1
        out.append(-solve(g, h, 2, empty - 1))
        h[c] -= 1
        g[r][c] = 0
    return out

def fires(b):
    if b.ply <= 9:
        return len(b.their_playable_wins) >= 2 or len(b.my_playable_wins) >= 2
    n = len(b.legal)
    if n > 3 or b.ply < 28:
        return False
    mv = move_values(b)
    if mv is None:
        return False
    if n <= 2:
        return not all(v == 1 for v in mv)
    return max(mv) == -1 and b.ply >= 31

def level(b):
    if b.ply <= 9:
        return 8 if fires(b) else 0
    n = len(b.legal)
    if b.ply < 26:
        return 0
    if n > 3:
        return 2 if b.ply >= 30 else 1
    mv = move_values(b)
    if mv is None:
        return 2
    if fires(b):
        return 9 if max(mv) == -1 else 7
    if all(v == 1 for v in mv):
        return 3
    return 4
