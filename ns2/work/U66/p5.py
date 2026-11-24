def vert5(b):
    h = b.heights[5]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][5] == 2 for k in range(3))

def blocked(b, c):
    r = b.landing(c)
    if r is None:
        return True
    return (r + 1, c) in b.their_wins

def center_closed(b):
    if b.landing(5) is None or blocked(b, 5):
        return False
    if b.my_playable_wins or b.their_playable_wins:
        return False
    return b.ply <= 30 and b.heights[2] == 6 and b.heights[3] == 6 and blocked(b, 4)

def fires(b):
    return vert5(b) or center_closed(b)

def level(b):
    if vert5(b):
        return 9 if b.last_col == 5 else 6
    if center_closed(b):
        return 5
    return 0
