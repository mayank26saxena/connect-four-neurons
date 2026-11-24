def _four(g, r, c, p):
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


def _dbl(b, p):
    # number of moves for player p that create two or more playable winning cells
    g = [row[:] for row in b.grid]
    cnt = 0
    for c in b.legal:
        r = b.heights[c]
        if _four(g, r, c, p):
            continue
        g[r][c] = p
        h = list(b.heights)
        h[c] += 1
        w = 0
        for cc in range(7):
            rr = h[cc]
            if rr < 6 and _four(g, rr, cc, p):
                w += 1
                if rr + 1 < 6 and _four(g, rr + 1, cc, p):
                    w += 1
        g[r][c] = 0
        if w >= 2:
            cnt += 1
    return cnt


def fires(b):
    return _dbl(b, 2) + _dbl(b, 1) > 0


def level(b):
    n = _dbl(b, 2) + _dbl(b, 1)
    return min(9, 4 * n)
