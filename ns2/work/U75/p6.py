def block_score(b):
    # cols 2-3, rows 0-1: col2 empty or capped by them at row 1; col3 empty or mine at row 1 (best on their stone)
    g = b.grid
    h2 = b.heights[2]
    h3 = b.heights[3]
    s = 0
    if h2 == 0:
        s += 2
    elif h2 == 2 and g[1][2] == 2:
        s += 3 if g[0][2] == 1 else 2
    elif h2 == 3 and g[1][2] == 2 and g[2][2] == 2:
        s += 3
    else:
        return 0
    if h3 == 0:
        s += 2
    elif h3 == 2 and g[1][3] == 1:
        s += 3 if g[0][3] == 2 else 1
    elif h3 >= 3 and g[1][3] == 1:
        s += 1
    else:
        return 0
    return s

def fires(b):
    if b.my_playable_wins:
        return False
    return b.me_first and b.ply <= 18 and block_score(b) >= 4

def level(b):
    if b.my_playable_wins:
        return 0
    s = block_score(b)
    if not b.me_first:
        s -= 2
    if b.ply > 18:
        s -= 2
    return max(0, min(9, s * 2 - 3))
