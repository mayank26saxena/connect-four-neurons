def feats(b):
    o1 = sum(1 for c in range(1, 6) if b.grid[1][c] == 2)
    x1 = sum(1 for c in range(7) if b.grid[1][c] == 1)
    xhi = sum(1 for r in range(1, 6) for c in range(7) if b.grid[r][c] == 1)
    return o1, x1, xhi

def fires(b):
    if b.ply > 14 or len(b.their_playable_wins) > 0:
        return False
    o1, x1, xhi = feats(b)
    if xhi == 0 and b.ply >= 5 and (o1 >= 1 or (b.grid[0][1] == 2 and b.grid[0][2] == 1)):
        return True
    return o1 >= 2 and x1 == 0

def level(b):
    if not fires(b):
        return 0
    o1, x1, xhi = feats(b)
    return min(9, 4 + 2 * o1 - xhi)
