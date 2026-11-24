def cell_score(b, r, c):
    s = 0
    for dr, dc in [(0, 1), (1, 1), (1, -1)]:
        for k in range(4):
            cells = [(r + (i - k) * dr, c + (i - k) * dc) for i in range(4)]
            if not all(0 <= rr < 6 and 0 <= cc < 7 for rr, cc in cells):
                continue
            v = [b.grid[rr][cc] for rr, cc in cells if (rr, cc) != (r, c)]
            if 1 in v:
                continue
            n = v.count(2)
            s += [0, 0, 2, 6][n]
    return s

def score5(b):
    if b.heights[5] != 0:
        return 0
    return cell_score(b, 1, 5)

def fires(b):
    return score5(b) >= 4

def level(b):
    return min(9, score5(b))
