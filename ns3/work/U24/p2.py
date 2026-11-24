def fires(b):
    # opponent just played in the centre column and centre column has my stone at the bottom
    return b.last_col == 3 and b.heights[0] <= 1 and b.heights[6] <= 1

def level(b):
    s = 0
    if b.last_col == 3:
        s += 3
    elif b.last_col in (2, 4):
        s += 1
    if b.heights[0] <= 1:
        s += 1
    if b.heights[6] <= 1:
        s += 1
    if b.grid[0][3] == 1:
        s += 1
    if b.grid[1][3] == 1:
        s += 1
    if b.grid[2][3] == 2:
        s += 1
    return min(9, s)
