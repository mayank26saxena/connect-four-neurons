def split_window(b, cells):
    v = [b.grid[r][c] for (r, c) in cells]
    if 2 in v or v.count(1) < 2 or v.count(1) == 4:
        return 0
    idx = [i for i in range(4) if v[i] == 1]
    gap = any(v[i] == 0 for i in range(idx[0] + 1, idx[-1]))
    return v.count(1) if gap else 0

def anti_score(b):
    k = 0
    for r in range(3):
        for c in range(3, 7):
            cells = [(r + i, c - i) for i in range(4)]
            k = max(k, split_window(b, cells))
    return k

def row0_score(b):
    if b.grid[0][3] != 0:
        return 0
    k = 0
    for s in range(4):
        v = [b.grid[0][c] for c in range(s, s + 4)]
        left = any(b.grid[0][c] == 1 for c in range(s, 3))
        right = any(b.grid[0][c] == 1 for c in range(4, s + 4))
        if 2 not in v and left and right:
            k = max(k, v.count(1))
    return k

def fires(b):
    if len(b.my_playable_wins) > 0:
        return False
    return anti_score(b) >= 2 or row0_score(b) >= 2

def level(b):
    if not fires(b):
        return 0
    return 7 if anti_score(b) >= 3 else 5
