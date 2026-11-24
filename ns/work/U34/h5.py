def opp_score(b):
    s = 0
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    seen = set()
    for r in range(6):
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

def fires(b):
    return b.heights[5] == 0 and opp_score(b) >= 3

def level(b):
    if b.heights[5] != 0:
        return 0
    return min(9, opp_score(b) * 2)
