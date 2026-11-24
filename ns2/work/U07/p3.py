def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def side(b):
    ol = 0
    orr = 0
    for r in range(6):
        for c in range(7):
            if b.grid[r][c] == 2:
                if c < 3:
                    ol += 1
                elif c > 3:
                    orr += 1
    return ol, orr

def fires(b):
    if b.my_playable_wins and not vert3(b, 3):
        return False
    if b.last_col == 3 and vert3(b, 3):
        return True
    if b.heights[3] == 0:
        ol, orr = side(b)
        return ol >= 2 and ol > orr
    return False

def level(b):
    if b.last_col == 3 and vert3(b, 3) and not b.my_playable_wins:
        return 9
    if b.heights[3] == 0:
        ol, orr = side(b)
        if ol >= 2 and ol > orr:
            return 6
        return 3
    return 0
