def colcount(b, who, c):
    return sum(1 for r in range(6) if b.grid[r][c] == who)

def early(b):
    if b.ply == 2:
        return 4 if (b.grid[0][4] == 2 and b.last_col == 4 and b.moves[0] == 4 and b.moves[1] in (3, 4, 5)) else 0
    if b.ply % 2 == 0 or b.ply > 9:
        return 0
    oc = colcount(b, 2, 3) + colcount(b, 2, 4)
    o5 = colcount(b, 2, 5)
    if colcount(b, 1, 1) > 0:
        return 0
    s = 0
    if oc >= 2:
        s = 6
    elif oc >= 1 and o5 >= 1:
        s = 4
    else:
        return 0
    if b.ply >= 7:
        s -= 2
    return s

def fires(b):
    return early(b) >= 3

def level(b):
    return early(b)
