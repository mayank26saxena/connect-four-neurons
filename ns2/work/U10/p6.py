def vthree(b, c):
    # opponent's top three stones in column c, cell above empty
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    if b.my_playable_wins:
        return False
    return vthree(b, 2) or vthree(b, 3)

def level(b):
    if not b.my_playable_wins and vthree(b, 2):
        return 9
    if fires(b):
        return 6
    if any(vthree(b, c) for c in (4, 5, 6)):
        return 3
    return 0
