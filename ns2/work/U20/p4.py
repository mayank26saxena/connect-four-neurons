def control(b):
    mine = 0
    theirs = 0
    for c in b.legal:
        for r in range(b.landing(c), 6):
            t = (r, c) in b.their_wins
            m = (r, c) in b.my_wins
            if t or m:
                if t and not m:
                    theirs += 1
                elif m and not t:
                    mine += 1
                break
    return mine, theirs

def fires(b):
    if b.heights[4] < 6:
        return False
    m, t = control(b)
    return t > m

def level(b):
    if b.heights[4] < 6:
        return 0
    m, t = control(b)
    s = 2 + 3 * (t > m) + (b.heights[5] == 6) + (b.heights[3] == 6) + (t - m > 1)
    return min(9, s)
