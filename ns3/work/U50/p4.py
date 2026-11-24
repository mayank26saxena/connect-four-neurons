def horiz_threats(b):
    out = set()
    for r in range(6):
        for s in range(4):
            cells = [b.grid[r][s + k] for k in range(4)]
            if cells.count(1) == 3 and cells.count(0) == 1:
                c = s + cells.index(0)
                if r - 1 >= b.heights[c] and (r - 1, c) in b.their_wins:
                    continue
                out.add((r, c))
    return out

def fires(b):
    return len(horiz_threats(b)) > 0

def level(b):
    t = horiz_threats(b)
    if not t:
        return 0
    s = 5
    if any(c == 6 for (r, c) in t):
        s += 3
    if len(t) > 1:
        s += 1
    return min(9, s)
