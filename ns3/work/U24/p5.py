def cross(b):
    # count 2x2 squares in columns 3-4 where my stones run up-right (r,3),(r+1,4)
    # and their stones run up-left (r,4),(r+1,3)
    g = b.grid
    n = 0
    for r in range(5):
        if g[r][3] == 1 and g[r + 1][4] == 1 and g[r][4] == 2 and g[r + 1][3] == 2:
            n += 1
    return n

def fires(b):
    return cross(b) >= 1

def level(b):
    n = cross(b)
    if n == 0:
        return 0
    s = 4 + 2 * n
    if b.last_col in (3, 4):
        s += 1
    return min(9, s)
