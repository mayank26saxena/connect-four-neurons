def mine_by_col(b):
    m = [0] * 7
    for r in range(6):
        for c in range(7):
            if b.grid[r][c] == 1:
                m[c] += 1
    return m

def early(b):
    if b.ply > 8 or b.last_col in (5, 6):
        return False
    m = mine_by_col(b)
    good = m[1] + m[3]
    other = sum(m) - good
    bad = m[4] + m[6]
    return good >= 1 and other <= (1 if b.ply <= 6 else 0) and bad <= (1 if good >= 2 and b.ply <= 6 else 0) and good >= other

def late(b):
    return b.ply > 6 and b.last_col == 3 and b.last_row == 5

def fires(b):
    if b.last_col is None or b.ply < 4:
        return False
    return early(b) or late(b)

def level(b):
    if b.last_col is None or b.ply < 4:
        return 0
    if early(b):
        m = mine_by_col(b)
        lv = 5 + (m[1] + m[3]) + (1 if b.last_col in (0, 3, 4) else 0) - (b.ply - 4) // 2
        return max(1, min(9, lv))
    if late(b):
        return 5
    if b.last_row == 5:
        return 2
    return 0
