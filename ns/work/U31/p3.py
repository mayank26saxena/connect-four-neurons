OPEN2 = {(0, 0), (0, 6), (1, 1), (3, 6), (4, 0), (4, 4), (4, 5), (4, 6), (5, 5), (5, 6), (6, 0), (6, 5), (6, 6)}

def col(b, c):
    return [b.grid[r][c] for r in range(6)]

def strength(b):
    s = 0
    c5 = col(b, 5)
    if c5[0] == 1 and c5[1] == 1 and c5[2] == 1 and c5[3] == 2:
        s = max(s, 9)
    elif c5[1] == 1 and c5[2] == 1 and c5[3] == 2:
        s = max(s, 7)
    c3 = col(b, 3)
    if c3[1] == 1 and c3[2] == 1 and c3[3] == 2:
        s = max(s, 7)
    if b.ply == 2 and tuple(b.moves) in OPEN2:
        s = max(s, 5)
    return s

def fires(b):
    return strength(b) >= 5

def level(b):
    return strength(b)
