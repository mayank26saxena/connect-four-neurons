def wins_for(g, p):
    out = set()
    for r in range(6):
        for c in range(7):
            if g[r][c] != 0:
                continue
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                n = 1
                for s in (1, -1):
                    rr, cc = r + s * dr, c + s * dc
                    while 0 <= rr < 6 and 0 <= cc < 7 and g[rr][cc] == p:
                        n += 1
                        rr += s * dr
                        cc += s * dc
                if n >= 4:
                    out.add((r, c))
                    break
    return out

def danger(b):
    # how much the opponent gains at the cell above column 5's landing cell if I play column 5
    r = b.landing(5)
    if r is None or r + 1 > 5:
        return 0
    if b.my_playable_wins or b.their_playable_wins:
        return 0
    if (r + 1, 5) in b.their_wins:
        return 3
    g = [row[:] for row in b.grid]
    g[r][5] = 1
    before = wins_for(g, 2)
    g[r + 1][5] = 2
    after = wins_for(g, 2)
    new = after - before
    return min(2, len(new))

def fires(b):
    return b.heights[5] <= 1 and danger(b) >= 2

def level(b):
    d = danger(b)
    if b.heights[5] > 1:
        d = min(d, 1)
    return [0, 3, 7, 9][d]
