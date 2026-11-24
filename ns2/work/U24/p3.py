DIRS = ((0, 1), (1, 0), (1, 1), (1, -1))

def win_at(g, r, c, p):
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

def land(g, c):
    for r in range(6):
        if g[r][c] == 0:
            return r
    return None

def playable_wins(g, p):
    out = []
    for c in range(7):
        r = land(g, c)
        if r is not None and win_at(g, r, c, p):
            out.append(c)
    return out

def loses(g, c):
    # I (1) play c; does the opponent (2) then win by force within their next move + one more?
    r = land(g, c)
    g[r][c] = 1
    bad = False
    if win_at(g, r, c, 1):
        g[r][c] = 0
        return False
    if playable_wins(g, 2):
        bad = True
    else:
        for c2 in range(7):
            r2 = land(g, c2)
            if r2 is None:
                continue
            g[r2][c2] = 2
            w = playable_wins(g, 2)
            mine = playable_wins(g, 1)
            g[r2][c2] = 0
            if len(set(w)) >= 2 and not mine:
                bad = True
                break
            if len(w) == 1 and not mine:
                # forced block; does blocking hand them the cell above?
                cb = w[0]
                rb = land(g, cb)
                g[r2][c2] = 2
                g[rb][cb] = 1
                w2 = playable_wins(g, 2)
                g[rb][cb] = 0
                g[r2][c2] = 0
                if w2 and not win_at(g, rb, cb, 1):
                    bad = True
                    break
    g[r][c] = 0
    return bad

def safe_moves(b):
    g = [list(row) for row in b.grid]
    return [c for c in b.legal if not loses(g, c)]

def fires(b):
    if b.my_playable_wins:
        return False
    s = safe_moves(b)
    return len(s) == 1

def level(b):
    if b.my_playable_wins:
        return 0
    s = safe_moves(b)
    if len(s) == 1:
        if (b.heights[3], 3) in b.their_playable_wins and b.heights[3] >= 4:
            return 9
        return 6
    if len(s) == 2:
        return 2
    return 0
