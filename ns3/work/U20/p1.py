def col2_threat(b):
    best = 0
    for (r, c) in b.their_playable_wins:
        if c != 2:
            continue
        # vertical: three of theirs below
        if r >= 3 and all(b.grid[r - k][2] == 2 for k in (1, 2, 3)):
            best = max(best, 9)
            continue
        # diagonal
        for dr, dc in ((1, 1), (1, -1)):
            n = 0
            for s in (1, -1):
                rr, cc = r + s * dr, c + s * dc
                while 0 <= rr < 6 and 0 <= cc < 7 and b.grid[rr][cc] == 2:
                    n += 1
                    rr += s * dr
                    cc += s * dc
            if n >= 3:
                best = max(best, 6)
    return best

def fires(b):
    return col2_threat(b) > 0

def level(b):
    return col2_threat(b)
