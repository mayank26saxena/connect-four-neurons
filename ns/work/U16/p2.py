def col0_row_of(b, k):
    # row at which the k-th most recent move (k=1 is the last) landed, if it was in column 0; else None
    if len(b.moves) < k or b.moves[-k] != 0:
        return None
    return sum(1 for m in b.moves[:len(b.moves) - k] if m == 0)

def fires(b):
    r1 = col0_row_of(b, 1)
    if r1 in (3, 4):
        return True
    r2 = col0_row_of(b, 2)
    return r2 in (3, 4) and b.last_col != 0

def level(b):
    r1 = col0_row_of(b, 1)
    if r1 == 4:
        return 9
    if r1 == 3:
        return 6
    if r1 == 5:
        return 2
    r2 = col0_row_of(b, 2)
    if r2 in (3, 4) and b.last_col != 0:
        return 4
    return 0
