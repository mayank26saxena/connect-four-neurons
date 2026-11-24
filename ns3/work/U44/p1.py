def vthree(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return level(b) >= 3

def level(b):
    if vthree(b, 1):
        return 9
    land = b.landing(1)
    if land is not None and (land, 1) in b.their_playable_wins:
        return 5
    if vthree(b, 5):
        return 4
    return 0
