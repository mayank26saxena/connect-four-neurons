def col1_theirs(b):
    # the stone just played is in column 1 and every stone in column 1 is theirs (none of mine)
    return b.last_col == 1 and all(b.grid[r][1] != 1 for r in range(b.heights[1]))

def col1_hit(b):
    if not col1_theirs(b):
        return False
    return b.heights[1] == 1 or (b.heights[1] == 2 and b.ply <= 6)

def opening4(b):
    # 4-stone opening, all stones in different columns, column 1 untouched
    return b.ply == 4 and len(set(b.moves)) == 4 and b.heights[1] == 0

def fires(b):
    return col1_hit(b) or opening4(b)

def level(b):
    if col1_hit(b):
        if b.heights[1] == 2:
            return 6
        if b.ply <= 4:
            return 9
        if b.ply <= 7:
            return 7
        return 5
    if col1_theirs(b) and b.heights[1] == 2:
        return 3
    if opening4(b):
        return 3
    if b.ply == 4 and b.heights[1] == 0:
        return 2
    return 0
