def vthree6(b):
    h = b.heights[6]
    if h < 3 or h >= 6:
        return 0
    if all(b.grid[h - 1 - k][6] == 2 for k in range(3)):
        return h
    return 0

def two6(b):
    # opponent just played col 6 on top of their own stone, column not high, no other urgent tactics
    h = b.heights[6]
    if b.last_col != 6 or h < 2 or h > 4:
        return False
    if b.grid[h - 2][6] != 2:
        return False
    if b.my_playable_wins:
        return False
    if any(c != 6 for (r, c) in b.their_playable_wins):
        return False
    return True

def fires(b):
    return vthree6(b) > 0 or two6(b)

def level(b):
    h = vthree6(b)
    if h:
        v = {3: 9, 4: 7, 5: 6}[h]
        if b.my_playable_wins:
            v -= 3
        return v
    if two6(b):
        return 3
    return 0
