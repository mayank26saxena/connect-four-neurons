KEY = [((2, 2), 1), ((1, 4), 1), ((2, 4), 2), ((0, 4), 2), ((0, 5), 2), ((1, 5), 1), ((0, 2), 1)]

def score(b):
    g = b.grid
    if g[1][2] != 2 or b.heights[0] > 1 or b.heights[1] > 1 or g[0][0] == 1:
        return 0
    k = 1
    for (r, c), v in KEY:
        if g[r][c] == v:
            k += 1
    if g[0][1] != 0:
        k += 1
    return k

def fires(b):
    return score(b) >= 4

def level(b):
    return max(0, min(9, score(b) + 1)) if score(b) > 0 else 0
