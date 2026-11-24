def cnt(b, who, cols):
    return sum(1 for r in range(6) for c in cols if b.grid[r][c] == who)

def early(b):
    if b.ply == 2:
        return 4 if (b.moves[0] == 4 and b.moves[1] in (3, 4, 5) and b.grid[0][4] == 2 and b.last_col == 4) or b.moves == [4, 3] else 0
    if b.ply not in (3, 5):
        return 0
    if cnt(b, 1, [1]) > 0:
        return 0
    o4 = cnt(b, 2, [4])
    oc = cnt(b, 2, [3, 4, 5])
    m4 = cnt(b, 1, [4])
    s = 0
    if m4 > 0 and oc >= 2:
        s = 9
    elif o4 >= 1 and cnt(b, 2, [3, 4, 5, 6]) >= 2:
        s = 7
    elif m4 > 0 and cnt(b, 2, [2, 3, 5, 6]) >= 1:
        s = 4
    if b.ply == 5:
        s -= 2
        if b.last_col not in (3, 4, 5):
            s -= 3
    return max(s, 0)

def fires(b):
    return early(b) >= 4

def level(b):
    return early(b)
