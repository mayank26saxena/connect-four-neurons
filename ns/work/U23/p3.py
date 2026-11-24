def wins_at(g, r, c, p):
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

def losing_moves(b):
    # count my legal moves after which the opponent can win immediately
    g = [list(row) for row in b.grid]
    h = list(b.heights)
    lose = 0
    for m in b.legal:
        r = h[m]
        if wins_at(g, r, m, 1):
            return -1
        g[r][m] = 1
        h[m] += 1
        bad = False
        for c in range(7):
            if h[c] < 6 and wins_at(g, h[c], c, 2):
                bad = True
                break
        g[r][m] = 0
        h[m] -= 1
        if bad:
            lose += 1
    return lose

def fires(b):
    if not b.legal:
        return False
    return losing_moves(b) == len(b.legal)

def level(b):
    if not b.legal:
        return 0
    l = losing_moves(b)
    if l == len(b.legal):
        return 8
    if l < 0:
        return 2
    return min(4, l)
