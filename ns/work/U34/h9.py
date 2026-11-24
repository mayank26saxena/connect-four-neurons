def opp_score(b):
    s = 0
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    seen = set()
    for r in range(2):
        if b.grid[r][5] != 0:
            continue
        for dr, dc in dirs:
            for k in range(4):
                r0, c0 = r - k * dr, 5 - k * dc
                cells = [(r0 + i * dr, c0 + i * dc) for i in range(4)]
                if not all(0 <= rr < 6 and 0 <= cc < 7 for rr, cc in cells):
                    continue
                key = tuple(cells)
                if key in seen:
                    continue
                seen.add(key)
                v = [b.grid[rr][cc] for rr, cc in cells]
                if 1 in v:
                    continue
                n = v.count(2)
                if n >= 2:
                    s += n - 1
    return s
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
    if False:
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

def total(b):
    if b.heights[5] != 0:
        return 0
    if (1, 5) not in b.their_wins:
        if (2, 5) in b.their_wins or b.their_playable_wins or b.my_playable_wins:
            return 0
    return opp_score(b) + 2 * danger(b)

def fires(b):
    return total(b) >= 5

def level(b):
    return min(9, total(b))
