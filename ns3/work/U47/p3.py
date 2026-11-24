def windows0():
    # every 4-cell line that contains a column-0 cell: horizontal cols 0-3, and the two diagonals starting in column 0
    out = []
    for r in range(6):
        out.append([(r, c) for c in range(4)])
        if r + 3 < 6:
            out.append([(r + k, k) for k in range(4)])
        if r - 3 >= 0:
            out.append([(r - k, k) for k in range(4)])
    for r in range(3):
        out.append([(r + k, 0) for k in range(4)])
    return out

WINS = windows0()

def left_score(b):
    s = 0
    for w in WINS:
        vals = [b.grid[r][c] for (r, c) in w]
        if 2 in vals:
            continue
        n = vals.count(1)
        if n == 3:
            # the missing cell is a col-0 threat; weight by how close it is to being playable
            (r, c) = [w[i] for i in range(4) if vals[i] == 0][0]
            h = b.landing(c)
            if h is None:
                continue
            d = r - h
            s += 6 if d == 0 else (4 if d == 1 else 1)
        elif n == 2:
            s += 1
    return s

def fires(b):
    if len(b.my_playable_wins) >= 2:
        return True
    return left_score(b) >= 4

def level(b):
    s = left_score(b)
    if len(b.my_playable_wins) >= 2:
        s += 4
    return min(9, s // 2)
