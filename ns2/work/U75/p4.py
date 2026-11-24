def points(b):
    g = b.grid
    h2 = b.heights[2]
    h3 = b.heights[3]
    p = 0
    if h2 == 0:
        p += 2
    elif h2 == 2 and g[1][2] == 2:
        p += 3
    elif h2 == 3 and g[1][2] == 2 and g[2][2] == 2:
        p += 3
    elif h2 % 2 == 1:
        p -= 2
    if h3 == 1:
        p -= 3
    if h3 >= 2 and g[1][3] == 1:
        p += 1
    if h3 >= 2 and g[1][3] == 2:
        p -= 1
    if g[0][1] == 1:
        p += 1
    if b.ply <= 14:
        p += 1
    if b.my_playable_wins:
        p -= 5
    return p

def fires(b):
    return points(b) >= 5

def level(b):
    p = points(b)
    return max(0, min(9, (p - 1) * 2))
