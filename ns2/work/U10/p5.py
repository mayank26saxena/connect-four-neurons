def vthree(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def threat(b):
    if b.my_playable_wins:
        return False
    return vthree(b, 2) or vthree(b, 3)

def opening(b):
    return b.ply <= 8 and b.grid[0][1] == 1

def fires(b):
    return threat(b) or opening(b)

def level(b):
    if vthree(b, 2) and not b.my_playable_wins:
        return 9
    if threat(b):
        return 6
    if opening(b):
        return 5
    return 0
