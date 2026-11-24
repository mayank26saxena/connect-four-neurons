def _win_at(g, r, c, p):
    for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
        n = 1
        rr, cc = r + dr, c + dc
        while 0 <= rr < 6 and 0 <= cc < 7 and g[rr][cc] == p:
            n += 1
            rr += dr
            cc += dc
        rr, cc = r - dr, c - dc
        while 0 <= rr < 6 and 0 <= cc < 7 and g[rr][cc] == p:
            n += 1
            rr -= dr
            cc -= dc
        if n >= 4:
            return True
    return False


def _solve(g, h, p, empty, memo, budget):
    # negamax: +1 side p to move wins, 0 draw, -1 loses
    if empty == 0:
        return 0
    key = (p, tuple(tuple(row) for row in g))
    if key in memo:
        return memo[key]
    budget[0] -= 1
    if budget[0] < 0:
        return 0
    cols = [c for c in (3, 2, 4, 1, 5, 0, 6) if h[c] < 6]
    for c in cols:
        if _win_at(g, h[c], c, p):
            memo[key] = 100
            return 100
    q = 3 - p
    best = -1000
    for c in cols:
        r = h[c]
        g[r][c] = p
        h[c] += 1
        v = -_solve(g, h, q, empty - 1, memo, budget)
        if v > 0:
            v -= 1
        elif v < 0:
            v += 1
        h[c] -= 1
        g[r][c] = 0
        if v > best:
            best = v

    memo[key] = best
    return best


def _outcome(b):
    empty = 42 - b.ply
    if empty > 14:
        return None
    g = [list(row) for row in b.grid]
    h = list(b.heights)
    budget = [20000]
    v = _solve(g, h, 1, empty, {}, budget)
    if budget[0] < 0:
        return None
    return v


def fires(b):
    if b.heights[1] != 6:
        return False
    if b.my_playable_wins:
        return False
    v = _outcome(b)
    return v is not None and v < 0


def level(b):
    if b.heights[1] != 6:
        return 0
    v = _outcome(b)
    nfull = sum(1 for x in b.heights if x == 6)
    if v is not None and v < 0 and not b.my_playable_wins:
        return min(9, 3 + nfull)
    if v is None:
        return 1
    return 1
