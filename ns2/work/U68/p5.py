DIAG = [(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)]

def split_window(b, cells):
    # window with no opponent stone, >= 2 of my stones, and an empty cell between two of mine
    v = [b.grid[r][c] for (r, c) in cells]
    if 2 in v or v.count(1) < 2 or v.count(1) == 4:
        return 0
    idx = [i for i in range(4) if v[i] == 1]
    gap = any(v[i] == 0 for i in range(idx[0] + 1, idx[-1]))
    return v.count(1) if gap else 0

def diag_score(b):
    k = 0
    for s in range(2):
        k = max(k, split_window(b, DIAG[s:s + 4]))
    return k

def row0_score(b):
    if b.grid[0][3] != 0:
        return 0
    k = 0
    for s in range(4):
        cells = [(0, c) for c in range(s, s + 4)]
        if s <= 3 <= s + 3:
            v = [b.grid[0][c] for c in range(s, s + 4)]
            left = any(b.grid[0][c] == 1 for c in range(s, 3))
            right = any(b.grid[0][c] == 1 for c in range(4, s + 4))
            if 2 not in v and left and right:
                k = max(k, v.count(1))
    return k

def fires_old(b):
    if len(b.my_playable_wins) > 0:
        return False
    return diag_score(b) >= 2 or row0_score(b) >= 2

def level(b):
    if not fires(b):
        return 0
    return 7 if diag_score(b) >= 3 else 6

def fires(b):
    if len(b.my_playable_wins) > 0:
        return False
    if row0_score(b) >= 2 and b.ply <= 8:
        return True
    return diag_score(b) >= 2 and b.grid[2][2] == 0 and b.heights[2] <= 1 and b.heights[0] <= 3
