def s(b):
    # crude left/right score seen in a 4-stone sweep, plus early-game and parity
    v = 0.0
    if b.grid[1][0] == 2: v += 2
    if b.grid[0][0] == 1: v += 1
    if b.grid[0][1] == 1: v += 0.5
    if b.grid[0][6] == 2: v -= 1.5
    if b.grid[0][2] == 2: v -= 0.7
    if b.last_col in (3, 4, 5): v += 0.7
    if b.me_first: v += 0.5
    v -= 0.25 * max(0, b.ply - 6)
    return v

def fires(b):
    return s(b) >= 1.5

def level(b):
    return max(0, min(9, int(round(2 * s(b)))))
