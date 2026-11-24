def line_len(b, r, c, dr, dc, p):
    n = 1
    for s in (1, -1):
        rr = r + s * dr
        cc = c + s * dc
        while 0 <= rr < 6 and 0 <= cc < 7 and b.grid[rr][cc] == p:
            n += 1
            rr += s * dr
            cc += s * dc
    return n

def nonvert_blocks(b):
    k = 0
    for (r, c) in b.their_playable_wins:
        for d in ((0, 1), (1, 1), (1, -1)):
            if line_len(b, r, c, d[0], d[1], 2) >= 4:
                k += 1
                break
    return k

def fires(b):
    # opponent threatens to win right now on a horizontal or diagonal line
    return nonvert_blocks(b) >= 1

def level(b):
    k = nonvert_blocks(b)
    if k >= 2:
        return 9
    if k == 1:
        return 7
    if b.their_playable_wins:
        return 3
    return 0
