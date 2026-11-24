def vertical_only(b, r, c):
    # True if the opponent's win at (r, c) only comes from three stacked stones below it
    g = b.grid
    vert = r >= 3 and all(g[r - k][c] == 2 for k in (1, 2, 3))
    if not vert:
        return False
    for dr, dc in ((0, 1), (1, 1), (1, -1)):
        n = 1
        for s in (1, -1):
            rr, cc = r + s * dr, c + s * dc
            while 0 <= rr < 6 and 0 <= cc < 7 and g[rr][cc] == 2:
                n += 1
                rr += s * dr
                cc += s * dc
        if n >= 4:
            return False
    return True

def high_blocks(b):
    return [(r, c) for (r, c) in b.their_playable_wins if r >= 4 and not vertical_only(b, r, c)]

def fires(b):
    if b.my_playable_wins:
        return False
    return len(high_blocks(b)) > 0

def level(b):
    if b.my_playable_wins:
        return 0
    hb = high_blocks(b)
    if any(c == 3 for r, c in hb):
        return 9
    if hb:
        return 6
    if b.landing(3) is not None and (b.heights[3] + 1, 3) in b.their_wins:
        return 0
    return 1
