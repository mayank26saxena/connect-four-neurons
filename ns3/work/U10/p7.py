DIRS = ((0, 1), (1, 0), (1, 1), (1, -1))

def wins_at(g, p, r, c):
    # would p placing at (r, c) complete four?
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

def land(h, c):
    return h[c] if h[c] < 6 else None

def win_moves(g, h, p):
    out = []
    for c in range(7):
        r = land(h, c)
        if r is not None and wins_at(g, p, r, c):
            out.append(c)
    return out

def loses_after(g, h, m):
    # I (1) play m; can the opponent (2) then win at once or set up an unstoppable threat?
    r = h[m]
    g[r][m] = 1
    h[m] += 1
    bad = False
    if win_moves(g, h, 2):
        bad = True
    else:
        for c in range(7):
            rr = land(h, c)
            if rr is None:
                continue
            g[rr][c] = 2
            h[c] += 1
            mine = win_moves(g, h, 1)
            if not mine:
                w = win_moves(g, h, 2)
                if len(w) >= 2:
                    bad = True
                elif len(w) == 1:
                    c2 = w[0]
                    r2 = h[c2]
                    if r2 + 1 < 6 and wins_at(g, 2, r2 + 1, c2):
                        bad = True
            g[rr][c] = 0
            h[c] -= 1
            if bad:
                break
    g[r][m] = 0
    h[m] -= 1
    return bad

def safe_list(b):
    g = [row[:] for row in b.grid]
    h = list(b.heights)
    return [m for m in b.legal if not loses_after(g, h, m)]

def critical_col(b):
    # the single column the position hinges on: my immediate win, a must-block, or the only move that does not lose
    if b.my_playable_wins:
        cols = sorted(set(c for r, c in b.my_playable_wins))
        return cols[0] if len(cols) == 1 else None
    if b.their_playable_wins:
        cols = sorted(set(c for r, c in b.their_playable_wins))
        return cols[0] if len(cols) == 1 else None
    s = safe_list(b)
    return s[0] if len(s) == 1 else None

def fires(b):
    return critical_col(b) in (2, 4)

def level(b):
    c = critical_col(b)
    if c == 4:
        return 9
    if c == 2:
        return 6
    if c is not None:
        return 1
    return 0
