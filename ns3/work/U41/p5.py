def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def makes4(g, r, c, p):
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

def their_fork_at1(b, col=1):
    # opponent drops in column col: how many immediate (or stacked, unstoppable) wins would they then have
    r = b.landing(col)
    if r is None:
        return 0
    g = [list(row) for row in b.grid]
    g[r][col] = 2
    h = list(b.heights)
    h[col] += 1
    k = 0
    for c in range(7):
        if h[c] < 6 and makes4(g, h[c], c, 2):
            k += 1
            if h[c] + 1 < 6:
                g2 = [list(row) for row in g]
                g2[h[c]][c] = 1
                if makes4(g2, h[c] + 1, c, 2):
                    k += 1
    return k

def level(b):
    r = b.landing(1)
    if r is None or len(b.my_playable_wins) > 0:
        return 0
    n = len(b.their_playable_wins)
    if r >= 1 and (r, 1) in b.their_playable_wins:
        if vert3(b, 1):
            return 9 if n == 1 else 5
        if n == 1 and r <= 3 and (r + 1, 1) not in b.their_wins:
            return 6
        return 0
    if n == 0 and their_fork_at1(b) >= 2:
        return 4
    return 0

def fires(b):
    return level(b) > 0
