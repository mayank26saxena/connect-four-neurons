def vert1(b):
    h = b.heights[1]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][1] == 2 for k in range(3))

def diag_win(b, r, c):
    for dr in (1, -1):
        for s in range(4):
            ok = True
            for k in range(4):
                rr = r + (k - s) * dr
                cc = c + (k - s)
                if rr < 0 or rr > 5 or cc < 0 or cc > 6:
                    ok = False
                    break
                if (rr, cc) != (r, c) and b.grid[rr][cc] != 2:
                    ok = False
                    break
            if ok:
                return True
    return False

def diag1(b):
    return any(c == 1 and diag_win(b, r, c) for (r, c) in b.their_playable_wins)

def fires(b):
    return vert1(b) or diag1(b)

def level(b):
    if vert1(b):
        return 9
    if diag1(b):
        return 4
    return 0
