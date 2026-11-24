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

ORDER = (3, 2, 4, 1, 5, 0, 6)

def solve(g, h, p, memo, alpha, beta):
    # value for player p to move: 1 win, 0 draw, -1 loss
    legal = [c for c in ORDER if h[c] < 6]
    if not legal:
        return 0
    for c in legal:
        if wins_at(g, h[c], c, p):
            return 1
    key = (tuple(tuple(row) for row in g), p)
    if key in memo:
        return memo[key]
    q = 3 - p
    best = -1
    for c in legal:
        r = h[c]
        g[r][c] = p
        h[c] += 1
        v = -solve(g, h, q, memo, -beta, -alpha)
        h[c] -= 1
        g[r][c] = 0
        if v > best:
            best = v
        if best > alpha:
            alpha = best
        if alpha >= beta:
            break
    if alpha < beta or best == 1:
        memo[key] = best
    return best

def value(b):
    g = [list(row) for row in b.grid]
    h = list(b.heights)
    return solve(g, h, 1, {}, -1, 1)

def fires_old(b):
    if b.ply < 28:
        return False
    return value(b) < 0

def level_old(b):
    if b.ply < 28:
        return 0
    v = value(b)
    if v < 0:
        return min(9, 4 + (b.ply - 28) // 2)
    return 0

def fires(b):
    if b.ply < 26 or len(b.legal) > 3:
        return False
    return value(b) < 0

def level(b):
    if not fires(b):
        return 0
    return {1: 9, 2: 6, 3: 3}[len(b.legal)]
