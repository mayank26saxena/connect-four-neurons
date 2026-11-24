def row0_double(b):
    for side in (1, 2):
        wins = b.my_playable_wins if side == 1 else b.their_playable_wins
        if len([w for w in wins if w[0] == 0]) >= 2:
            return True
    return False

def row0_pair(b):
    g = b.grid[0]
    empties = sum(1 for c in range(7) if g[c] == 0)
    for c in range(6):
        if g[c] != 0 and g[c] == g[c + 1]:
            s = g[c]
            l = c - 1
            r = c + 2
            if c + 2 < 7 and g[c + 2] == s:
                r = c + 3
            if l >= 0 and r < 7 and g[l] == 0 and g[r] == 0 and empties >= 4:
                return True
    return False

def fires(b):
    return row0_double(b) or row0_pair(b)

def level(b):
    if row0_double(b):
        return 9
    if row0_pair(b):
        return 5
    return 0
