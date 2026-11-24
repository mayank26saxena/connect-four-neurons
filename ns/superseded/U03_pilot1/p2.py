def fires(b):
    return 3 <= b.ply <= 10 and b.heights[3] <= 1 and b.grid[0][3] != 1

def level(b):
    if b.ply < 3:
        return 0
    s = 0
    if b.heights[3] == 0:
        s += 3
    elif b.heights[3] == 1 and b.grid[0][3] == 2:
        s += 2
    if b.ply <= 10:
        s += 3
    elif b.ply <= 16:
        s += 2
    elif b.ply <= 24:
        s += 1
    if any(c == 3 for r, c in b.my_wins | b.their_wins):
        s += 2
    if len(b.legal) == 7:
        s += 1
    return min(9, s)
