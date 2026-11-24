def col1_first(b):
    # the stone just played is the first stone in column 1
    return b.last_col == 1 and b.heights[1] == 1

def opening4(b):
    # 4-stone opening, all stones in different columns, column 1 untouched
    return b.ply == 4 and len(set(b.moves)) == 4 and b.heights[1] == 0

def fires(b):
    return col1_first(b) or opening4(b)

def level(b):
    if col1_first(b):
        if b.ply <= 4:
            return 9
        if b.ply <= 7:
            return 7
        return 5
    if b.last_col == 1 and b.heights[1] == 2 and b.grid[0][1] == 2:
        return 3
    if opening4(b):
        return 3
    if b.ply == 4 and b.heights[1] == 0:
        return 2
    return 0
