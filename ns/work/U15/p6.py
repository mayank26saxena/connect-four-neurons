def windows(b):
    g = b.grid
    mine = 0
    theirs = 0
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(6):
        for c in range(7):
            for dr, dc in dirs:
                er = r + 3 * dr
                ec = c + 3 * dc
                if er < 0 or er > 5 or ec < 0 or ec > 6:
                    continue
                cells = [g[r + k * dr][c + k * dc] for k in range(4)]
                n1 = cells.count(1)
                n2 = cells.count(2)
                if n1 > 0 and n2 == 0:
                    mine += n1
                if n2 > 0 and n1 == 0:
                    theirs += n2
    return mine, theirs

def raw(b):
    m, t = windows(b)
    s = (m - t) / 2.0
    if b.me_first:
        s += 2
    if b.ply <= 10:
        s += 1
    return s

def fires(b):
    return raw(b) >= 7

def level(b):
    return max(0, min(9, int(raw(b)) - 2))
