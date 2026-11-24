def g(b, r):
    return b.grid[r][0]

def kind(b):
    # A: their stone at row 3 of col 0 not covered by another of theirs
    if g(b, 3) == 2 and g(b, 4) != 2:
        return 1
    # B: their stone at row 4 sitting on my stone at row 3, not covered by theirs
    if g(b, 3) == 1 and g(b, 4) == 2 and g(b, 5) != 2:
        return 2
    return 0

def fires(b):
    k = kind(b)
    if k == 0:
        return False
    if k == 2:
        return True
    return b.last_col == 0 or (g(b, 2) == 1 and g(b, 1) == 1) or (g(b, 2) == 1 and b.ply <= 16)

def level(b):
    k = kind(b)
    if k == 0:
        return 0
    if k == 2:
        return 5
    if g(b, 2) != 1:
        return 3 if b.last_col == 0 else 2
    lv = 5
    if g(b, 1) == 1:
        lv += 1
    if b.ply <= 14:
        lv += 2
    if b.last_col == 0:
        lv += 1
    return min(lv, 9)
