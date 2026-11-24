def right_three(b):
    rows = []
    for r in range(6):
        if b.grid[r][3] == 1 and b.grid[r][4] == 1 and b.grid[r][5] == 1 and b.grid[r][6] == 0:
            if r - 1 >= b.heights[6] and (r - 1, 6) in b.their_wins:
                continue
            rows.append(r)
    return rows

def lost(b):
    return len(b.their_playable_wins) >= 2

def fires(b):
    return len(right_three(b)) > 0 or lost(b)

def level(b):
    if right_three(b):
        return 9
    if lost(b):
        return 6
    return 0
