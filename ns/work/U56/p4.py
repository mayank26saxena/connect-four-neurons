DIRS = [(1, 0), (0, 1), (1, 1), (1, -1)]

def uses_last(b, r, c):
    # the win cell (r, c) completes a four for them that includes the stone just played
    lr, lc = b.last_row, b.last_col
    if lr is None:
        return False
    for dr, dc in DIRS:
        for s in range(-3, 1):
            cells = [(r + (s + k) * dr, c + (s + k) * dc) for k in range(4)]
            if (r, c) not in cells or (lr, lc) not in cells:
                continue
            ok = True
            for (rr, cc) in cells:
                if rr < 0 or rr > 5 or cc < 0 or cc > 6:
                    ok = False
                    break
                if (rr, cc) != (r, c) and b.grid[rr][cc] != 2:
                    ok = False
                    break
            if ok:
                return True
    return False

def new_blocks(b):
    return [(r, c) for (r, c) in b.their_playable_wins if uses_last(b, r, c)]

def fires_old(b):
    return any(c == 6 and r >= 1 for (r, c) in new_blocks(b))

def level(b):
    nb = new_blocks(b)
    if any(c == 6 and r >= 1 for (r, c) in nb):
        return 9
    if any(c == 6 and r >= 1 for (r, c) in b.their_playable_wins):
        return 4
    if any(r >= 1 for (r, c) in nb):
        return 3
    return 0

def fires(b):
    return any(r >= 1 for (r, c) in new_blocks(b))
