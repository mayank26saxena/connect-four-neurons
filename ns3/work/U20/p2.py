def run(b, r, c, dr, dc):
    n = 0
    for s in (1, -1):
        rr, cc = r + s * dr, c + s * dc
        while 0 <= rr < 6 and 0 <= cc < 7 and b.grid[rr][cc] == 2:
            n += 1
            rr += s * dr
            cc += s * dc
    return n

def col2_threat(b):
    best = 0
    for (r, c) in b.their_playable_wins:
        if c != 2:
            continue
        if r >= 3 and all(b.grid[r - k][2] == 2 for k in (1, 2, 3)):
            best = max(best, 9)
        elif r >= 2 and (run(b, r, c, 1, 1) >= 3 or run(b, r, c, 1, -1) >= 3):
            best = max(best, 6)
        elif r >= 2:
            best = max(best, 4)
        else:
            best = max(best, 2)
    return best

def fires(b):
    return col2_threat(b) >= 4

def level(b):
    return col2_threat(b)
