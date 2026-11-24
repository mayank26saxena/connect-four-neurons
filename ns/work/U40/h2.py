def opening(b):
    if b.ply != 3:
        return False
    mine = [c for c in range(7) if b.grid[0][c] == 1]
    if not mine or mine[0] not in (2, 4, 6):
        return False
    return b.grid[0][5] != 2

def late(b):
    h = b.heights
    return b.ply >= 16 and h[5] == 6 and h[0] <= 3 and len(b.my_playable_wins) == 0

def fires(b):
    return opening(b) or late(b)

def level(b):
    if opening(b):
        return 9
    if late(b):
        return 6
    return 0
