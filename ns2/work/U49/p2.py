D = ((1, 0), (0, 1), (1, 1), (1, -1))

def wins(g, p):
    s = set()
    for r in range(6):
        for c in range(7):
            if g[r][c]:
                continue
            for dr, dc in D:
                cnt = 1
                for sg in (1, -1):
                    rr, cc = r + sg * dr, c + sg * dc
                    while 0 <= rr < 6 and 0 <= cc < 7 and g[rr][cc] == p:
                        cnt += 1
                        rr += sg * dr
                        cc += sg * dc
                if cnt >= 4:
                    s.add((r, c))
    return s

def creators(b, p):
    g = [list(row) for row in b.grid]
    base = wins(g, p)
    k = 0
    for c in b.legal:
        r = b.landing(c)
        g[r][c] = p
        if wins(g, p) - base:
            k += 1
        g[r][c] = 0
    return k

def score(b):
    s = 0
    if b.ply <= 20:
        s += 2
    if len(b.legal) == 7:
        s += 1
    s += min(3, creators(b, 2))
    s += min(2, creators(b, 1))
    if b.my_playable_wins or b.their_playable_wins:
        s -= 2
    return s

def fires(b):
    return score(b) >= 7

def level(b):
    return max(0, min(9, score(b)))
