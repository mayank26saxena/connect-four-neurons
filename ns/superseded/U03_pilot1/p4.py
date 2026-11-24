def bottom_three(b):
    # an empty bottom cell where my stone would give a 4-window on row 0 with 3 mine and none of theirs
    g = b.grid[0]
    for c in range(7):
        if g[c] != 0:
            continue
        for c0 in range(max(0, c - 3), min(3, c) + 1):
            w = [g[x] if x != c else 1 for x in range(c0, c0 + 4)]
            if 2 not in w and w.count(1) >= 3:
                return True
    return False

def fires(b):
    if any(r == 0 for r, c in b.my_playable_wins):
        return True
    return 3 <= b.ply <= 10 and b.heights[3] == 0

def level(b):
    if any(r == 0 for r, c in b.my_playable_wins):
        return 9
    if not (3 <= b.ply <= 12):
        return 0
    s = 0
    if b.heights[3] == 0:
        s += 4
    if bottom_three(b):
        s += 3
    if b.last_row is not None and b.last_row >= 1:
        s += 1
    return min(9, s)
