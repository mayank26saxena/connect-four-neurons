DIRS = ((0, 1), (1, 0), (1, 1), (1, -1))

def vthree(b, c, who):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == who for k in range(3))

def made_by_last(b, r, c):
    # is there a line of four through empty cell (r,c) whose other three are theirs and include the last stone?
    lr, lc = b.last_row, b.last_col
    if lr is None:
        return False
    for dr, dc in DIRS:
        for s in range(4):
            cells = [(r + (k - s) * dr, c + (k - s) * dc) for k in range(4)]
            if not all(0 <= rr < 6 and 0 <= cc < 7 for rr, cc in cells):
                continue
            others = [x for x in cells if x != (r, c)]
            if (lr, lc) in others and all(b.grid[rr][cc] == 2 for rr, cc in others):
                return True
    return False

def weak(b):
    for (r, c) in b.their_playable_wins:
        if c in (1, 2, 5) and made_by_last(b, r, c):
            return True
    return False

def fires(b):
    return vthree(b, 5, 2) or vthree(b, 5, 1) or weak(b)

def level(b):
    if vthree(b, 5, 2):
        return 9 if b.last_col == 5 else 6
    if vthree(b, 5, 1):
        return 3
    if weak(b):
        return 2
    return 0
