def vert6(b):
    h = b.heights[6]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][6] == 2 for k in range(3))

def threat6(b):
    # opponent has some empty cell in column 6 that would complete four for them,
    # and is not already winning elsewhere (no immediate threat outside column 6, not a double)
    if not any(c == 6 for (r, c) in b.their_wins):
        return False
    pw = b.their_playable_wins
    if len(pw) >= 2 or any(c != 6 for (r, c) in pw):
        return False
    return True

def fires(b):
    return vert6(b) or threat6(b)

def level(b):
    if vert6(b):
        if b.my_playable_wins:
            return 5
        return 9 if b.last_col == 6 else 4
    if threat6(b):
        return 3
    return 0
