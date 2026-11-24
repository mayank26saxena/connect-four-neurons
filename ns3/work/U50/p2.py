def hits(b):
    out = []
    for r in range(6):
        if b.grid[r][3] == 1 and b.grid[r][4] == 1 and b.grid[r][5] == 1 and b.grid[r][6] == 0:
            if r - 1 >= b.heights[6] and (r - 1, 6) in b.their_wins:
                continue
            out.append(r)
    return out

def fires(b):
    return len(hits(b)) > 0

def level(b):
    h = hits(b)
    if not h:
        return 0
    return 9 if min(h) > 0 else 6
