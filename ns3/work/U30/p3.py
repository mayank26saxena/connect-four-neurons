def opp_links(b):
    n = 0
    for r in range(6):
        for c in range(7):
            if b.grid[r][c] != 2:
                continue
            for dr, dc in [(0, 1), (1, 1), (1, -1)]:
                rr, cc = r + dr, c + dc
                if 0 <= rr < 6 and 0 <= cc < 7 and b.grid[rr][cc] == 2:
                    n += 1
    return n

def score(b):
    s = 0
    if b.ply <= 16:
        s += 2
    elif b.ply <= 22:
        s += 1
    if opp_links(b) <= 1:
        s += 1
    if b.heights[3] < 6 and b.heights[3] % 2 == 1:
        s += 1
    for (r, c) in [(1, 2), (2, 2), (1, 4), (2, 4)]:
        if b.grid[r][c] == 2:
            s -= 1
    return s

def fires(b):
    return score(b) >= 4

def level(b):
    return max(0, min(9, 2 * score(b)))
